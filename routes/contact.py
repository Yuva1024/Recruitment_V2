from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from models import Contact
from forms.contact import ContactForm

contact_bp = Blueprint('contact', __name__, url_prefix='/contact')

@contact_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    
    if form.validate_on_submit():
        message = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        
        db.session.add(message)
        
        try:
            db.session.commit()
            flash('Your message has been sent! We will get back to you soon.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error sending message: {str(e)}', 'danger')
    
    return render_template('contact.html', form=form, title='Contact Us')
