
"""Description: You are tasked with creating a Rectangle class with the following requirements:

An instance of the Rectangle class requires length:int and width:int to be initialized.
We can iterate over an instance of the Rectangle class 
When an instance of the Rectangle class is iterated over, we first get its length in the format: {'length': <VALUE_OF_LENGTH>} followed by the width {width: <VALUE_OF_WIDTH>}
"""

class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

# Example usage
rect = Rectangle(10, 5)

# Iterating over the Rectangle instance
for dimension in rect:
    print(dimension)


"""     Output:
        {'length': 10}
        {'width': 5}
"""


#Question 1: Are Django signals executed synchronously or asynchronously by default?
#Ans<------- Yes default, Django signals are executed synchronously, meaning that the signal handlers run in the same process and block the execution until they complete.

#python
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal handler started")
    time.sleep(5)  # Simulate a time-consuming task
    print("Signal handler finished")

## Create a new User instance
user = User.objects.create(username="testuser")
print("User created")
#Expected Output:
"""Signal handler started
    (after 5 seconds delay)
    Signal handler finished
    User created"""
#The "User created" message appears only after the signal handler completes its execution, proving that the signal runs synchronously.


"""<<<..........................................................................................................................>>>"""

#Question 2: Do Django signals run in the same thread as the caller?
#   Ans<---- Yes, by default, Django signals run in the same thread as the caller.


import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal handler thread ID: {threading.get_ident()}")

# Check the main thread ID
print(f"Main thread ID: {threading.get_ident()}")

# Create a new User instance
user = User.objects.create(username="testuser")
"""Expected Output:
    Main thread ID: 140735227442944
    Signal handler thread ID: 140735227442944"""  

"""<<<............................................................................................................................>>>"""

#Question 3: Do Django signals run in the same database transaction as the caller?
# Ans<---    Yes, by default, Django signals run in the same database transaction as the caller, but only for signals that are fired within a transaction block. This means that if the transaction is rolled back, the changes made by the signal handler will also be rolled back.

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    instance.first_name = "Changed"
    instance.save()
    print("Signal handler executed")

try:
    with transaction.atomic():
        user = User.objects.create(username="testuser")
        raise Exception("Forcing a rollback")  # Simulate an error

except Exception as e:
    print("Transaction rolled back")

# Check if changes made in the signal handler were saved
user_exists = User.objects.filter(username="testuser").exists()
print(f"User exists after rollback: {user_exists}")


"""Expected Output:

    Signal handler executed
    Transaction rolled back
    User exists after rollback: False"""

