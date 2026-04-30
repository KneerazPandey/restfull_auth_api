from django.contrib.auth.base_user import BaseUserManager


class AuthenticationUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        return user 
    
    def create_superuser(self, username, email, password, **kwargs):
        if not password:
            raise ValueError('Superuser must have password')
        
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_verified', True)
        
        if kwargs.get('is_staff') is not True:
            raise TypeError('Superuser must have is_staff=True')
        if kwargs.get('is_active') is not True:
            raise TypeError('Superuser must have is_active=True')
        if kwargs.get('is_superuser') is not True:
            raise TypeError('Superuser must have is_superuser=True')
        if kwargs.get('is_verified') is not True:
            raise TypeError('Superuser must have is_verified=True')
        
        return self.create_user(email=email, password=password, **kwargs)