# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
# Cas number verification
import cirpy
from wtforms.validators import DataRequired, Length, ValidationError

from .models import User, Experiment


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True

# Custom validator to check for alphanumeric characters
def alphanumeric(form, field):
    if not re.match("^[a-zA-Z0-9]*$", field.data):
        raise ValidationError('Field must contain only alphanumeric characters.')

def is_valid_protein(sequence):
    valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
    return all(residue in valid_amino_acids for residue in sequence.upper())

class UploadExperimentForm(FlaskForm):
    """Form for users to upload data to."""

    name = StringField(
        "name", validators=[DataRequired(), Length(min=3, max=15)]#), alphanumeric]
    )
    protein = StringField(
        "protein", validators=[DataRequired(), Length(min=6, max=10000)]
    )
    reaction = StringField("reaction")  # No validators since this is
    cas_substrate = StringField(
        "CAS substrate", validators=[DataRequired(), Length(min=1, max=1000)]
    )
    cas_product = StringField(
        "CAS product", validators=[DataRequired(), Length(min=1, max=1000)]
    )
    def __init__(self, *args, **kwargs):
        """Create instance."""
        self.product_smiles = None
        self.substrate_smiles = None
        super(UploadExperimentForm, self).__init__(*args, **kwargs)

    def validate(self, **kwargs):
        """Validate the Experiment form use https://cirpy.readthedocs.io/en/latest/."""
        experiment = Experiment.query.filter_by(name=self.name.data).first()
        if experiment:
            self.name.errors.append("Name already exists")
            return False
        # Potentially already include if a protein has been engineered
        # Also add in an error for the CAS numbers
        product = self.cas_product.data
        print("-----------------------")
        print(self.cas_product, self.cas_substrate)
        print("-----------------------")
        print(self.name)
        self.product_smiles = cirpy.resolve(product.strip(), 'smiles')
        cas_substrate = self.cas_substrate.data
        self.substrate_smiles = cirpy.resolve(cas_substrate.strip(), 'smiles')
        # Check it only contains amino acids
        if not is_valid_protein(self.protein.data):
            self.protein.errors.append("Protein is not valid")
        if len(self.product_smiles) < 1:
            self.cas_product.errors.append("Unable to resolve SMILES for product, please enter a valid CAS product")
            return False
        if len(self.substrate_smiles) < 1:
            self.cas_substrate.errors.append("Unable to resolve SMILES for product, please enter a valid CAS product")
        return True
