from django.db import models
import re

class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['uName']) < 1:
            errors['uNameRequired'] = "Please input a user name."
        
        if len(postData['email']) < 1:
            errors['emailRequired'] = "Please input a email."

        elif not EMAIL_REGEX.match(postData['email']):
            errors['emailInvalid'] = "Please input a real email."
        
        if len(postData['pWord']) < 6:
            errors['pWordRequired'] = "Password must contain at least 6 characters"

        if postData['pWord'] != postData['cpWord']:
            errors['pWordMatch'] = "Confirm PW did not match Password."

        return errors

    def loginValidator(self, postData):
        errors = {}
        emailMatch = User.objects.filter(email = postData['email'])

        if len(postData['email']) < 1:
            errors['emailRequired'] = "Email is needed to login"
        
        elif len(emailMatch) == 0:
            errors['emailNotFound'] = 'Please register this email first.'

        else:
            if emailMatch[0].password != postData['pWord']:
                errors['incorrectpWord'] = 'Incorrect Password. Please try again.'

        return errors


class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        errors = {}

        if len(postData['qSource']) < 2:
            errors['qSourceRequired'] = "Quoted by must contain at least 2 characters"

        if len(postData['qDescription']) < 10:
            errors['qdescriptionRequired'] = "Message must contain at least 10 characters"

        return errors

class User(models.Model):
    userName = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    source = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    uploadedBy = models.ForeignKey(User, related_name='quotes_uploaded', on_delete = models.CASCADE)
    favoritedBy = models.ManyToManyField(User, related_name="favorited_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()