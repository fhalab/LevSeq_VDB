# -*- coding: utf-8 -*-
"""User views."""
from flask_login import login_required, current_user
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
import json
import pandas as pd
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)
import cirpy
from .models import User, Experiment, Data
from levseq_vdb.user.forms import UploadExperimentForm
from levseq_vdb.utils import flash_errors
import os

import os
dir_path = '/app/levseq_vdb/'

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/upload", methods=['GET', 'POST'])
@login_required
def members():
    """Home page."""
    # Here we want to return the users' experiments that have been uploaded.
    user_id = current_user.id
    form = UploadExperimentForm(request.form)
    # Handle logging in
    if request.method == "POST":
        if validate_form:
            csv_file = request.files['levseq_file']
            # # this basically means we need to add an entry to the experiments database
            substrate = form.cas_substrate.data
            product = form.cas_product.data
            protein = form.protein.data
            name = form.name.data.replace(' ', '_')
            reaction = form.reaction.data
            # Probs should sanitize the name
            if not os.path.exists(f'{dir_path}/data/{user_id}/{name}'):
                if not os.path.exists(f'{dir_path}/data/'):
                    os.system(f'mkdir {dir_path}/data/')
                if not os.path.exists(f'{dir_path}/data/{user_id}/'):
                    os.system(f'mkdir {dir_path}/data/{user_id}')
                os.system(f'mkdir {dir_path}/data/{user_id}/{name}/')
            json_data = df.to_json(orient='records')

            json_meta = json.dumps({
                    "substrate": substrate,
                    "product": product,
                    "data": f'{dir_path}/data/{user_id}/{name}/{name}_data.csv',
                    "substrate_cas": substrate,
                    "product_cas": product,
                    "reaction": reaction,
                    "protein": protein,
                    "name": form.name.data
                })
            Experiment.create(
                name=form.name.data,
                user_created=current_user.id,
                meta=json_meta  # Change this to the path where the data are stored...
            )
            df = pd.read_csv(csv_file)
            df['group'] = [str(w[0]) for w in df['Well'].values]
            df['variable'] = [str(w[1:]) for w in df['Well'].values]
            df.to_csv(f'{dir_path}/data/{user_id}/{name}/{name}_data.csv')
            rows = df.values
            rows = [list(r) for r in rows]
            columns = [{'title': c} for c in df.columns]
            df_for_d3 = df.to_dict(orient='records')  # Each row becomes a dictionary
            numerical_df = df.select_dtypes(include=['number'])
            numerical_columns = [{'title': col} for col in numerical_df.columns]

            return render_template('public/heatmap.html',
                                    data=json.dumps({'columns': columns, 'rows': rows}),
                                    columns=numerical_columns,
                                    df=json.dumps(df_for_d3)
                                    )
    return render_template("users/members.html", form=form)

"""
OK I do hate myself a bit for this but couldn't work out how to extend the form so for now this
is fine. I'm so sorry to whoever reads this and has to pick up my technical debt
"""

def is_valid_protein(sequence):
    valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
    return all(residue in valid_amino_acids for residue in sequence.upper())


def validate_form(uploaded_form):
        """Validate the Experiment form use https://cirpy.readthedocs.io/en/latest/."""
        experiment = Experiment.query.filter_by(name=uploaded_form.name.data).first()
        if experiment:
            print('Failed because there was another experiment with that name.')
            return False
        # Potentially already include if a protein has been engineered
        # Also add in an error for the CAS numbers
        product = uploaded_form.cas_product.data
        print(uploaded_form.cas_product, uploaded_form.cas_substrate)
        print(uploaded_form.name)
        cas_substrate = uploaded_form.cas_substrate.data
        substrate_smiles = cirpy.resolve(cas_substrate.strip(), 'smiles')
        product_smiles = cirpy.resolve(product.strip(), 'smiles')

        # Check it only contains amino acids
        if not is_valid_protein(uploaded_form.protein.data):
            print('Failed because there was another experiment with that name.')
            return False
        if len(product_smiles) < 1:
            print("Unable to resolve CAS for substrate, please enter a valid CAS product")
            return False
        if len(substrate_smiles) < 1:
            print("Unable to resolve CAS for product, please enter a valid CAS product")
            return False
        return True


@blueprint.route('/get_data/<id>', methods=['GET', 'POST'])
@login_required
def get_data(id):
    # Get an experiment based on the ID, then we load this
    # make sure the user is the one who owns the experiment before returning it to the user 
     # Fetch all data for the given experiment
    user_id = current_user.id
    datasets = Experiment.query.filter_by(user_created=user_id).all()    
    rows = []
    data_belongs_to_user = False
    for data in datasets:
        # expand out the metadata
        print(data.meta)
        meta = json.loads(str(data.meta))
        reaction = meta['reaction']
        substrate = meta['substrate']
        product = meta['product']
        rows.append([data.user_created, data.name, data.id, reaction, substrate, product, str(data.created_at), 
                     f"<a href='/users/get_data/{data.id}'>load</a>"])
        if data.id == int(id):
            name = data.name.replace(' ', '_')
            data_belongs_to_user = True
            break
    if data_belongs_to_user:
    # Get the experiments 
        df = pd.read_csv(f'/data/{user_id}/{name}/{name}_data.csv')
        rows = df.values
        rows = [list(r) for r in rows]
        columns = [{'title': c} for c in df.columns]
        df_for_d3 = df.to_dict(orient='records')  # Each row becomes a dictionary
        numerical_df = df.select_dtypes(include=['number'])
        numerical_columns = [{'title': col} for col in numerical_df.columns]

        return render_template('public/heatmap.html',
                                data=json.dumps({'columns': columns, 'rows': rows}),
                                columns=numerical_columns,
                                df=json.dumps(df_for_d3)
                                )
    return "That experiment didn't belong to you."

@blueprint.route("/", methods=['GET', 'POST'])
@login_required
def experiments():
    # Fetch all data for the given experiment
    user_id = current_user.id
    datasets = Experiment.query.filter_by(user_created=user_id).all()    
    rows = []
    for data in datasets:
        # expand out the metadata
        if user_id == data.user_created:
            meta = json.loads(str(data.meta))
            reaction = meta['reaction']
            substrate = meta['substrate']
            product = meta['product']
            rows.append([data.user_created, data.name, data.id, reaction, substrate, product, str(data.created_at), f"<a href='/users/get_data/{data.id}'>load</a>"])
                    
    columns = [{"title": "user_created"},
               {"title": "name"},
               {"title": "experiment_id"},
               {"title": "reaction"},
               {"title": "substrate"},
               {"title": "product"},
               {"title": "created_at"},
               {"title": ""}]
    return render_template('users/experiments.html',
                        data=json.dumps({'columns': columns, 'rows': rows}),
                        columns=columns)