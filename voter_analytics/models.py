from django.db import models
from datetime import datetime

# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data for registered voters in the town of Newton, MA.
    Voter ID,First Name,Last Name, Street Number, Street Name, Apt Number
    Zip Code, DOB, Registration Date, Party Aff, Precinct number
    '''
    # unique identifier
    voter_id = models.CharField(max_length=20, unique=True)

    first_name = models.TextField()
    last_name = models.TextField()

    residential_street_number = models.CharField(max_length=10)
    residential_street_name = models.CharField(max_length=100)
    residential_apartment_number = models.CharField(max_length=10, blank=True, null=True)
    residential_zip_code = models.CharField(max_length=10)

    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=2)

    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField()


    def __str__(self):
        '''Return a string representation of an instance of a voter from this model.'''

        voter_name = f"{self.first_name} {self.last_name}"
        addr = f"{self.residential_street_number} {self.residential_street_name}"
        if self.residential_apartment_number:
            addr += f" Apt {self.residential_apartment_number}"

        voter_info = f"{voter_name}: ({self.voter_id}) - {addr}, {self.residential_zip_code}"
        return voter_info
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = '/Users/rubychen/Desktop/django/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
        fields = line.strip().split(',')

        try:
            # create a new instance of Voter object with this record from CSV
            voter = Voter(
                voter_id = fields[0],
                last_name = fields[1],
                first_name = fields[2],
                residential_street_number = fields[3],
                residential_street_name = fields[4],
                residential_apartment_number = fields[5],
                residential_zip_code = fields[6], 
                date_of_birth = datetime.strptime(fields[7], "%Y-%m-%d").date(),
                date_of_registration = datetime.strptime(fields[8], "%Y-%m-%d").date(),
                party_affiliation = fields[9].strip(),
                precinct_number = fields[10],
                v20state = fields[11].strip().upper() == 'TRUE',
                v21town = fields[12].strip().upper() == 'TRUE',
                v21primary = fields[13].strip().upper() == 'TRUE',
                v22general = fields[14].strip().upper() == 'TRUE',
                v23town = fields[15].strip().upper() == 'TRUE',
                voter_score = fields[16],
            )

            # save the instance to the database
            voter.save()
            print(f'Created a new voter: {voter}')
        
        except Exception as e:
            print(f"Skipped: {fields} error: {type(e).__name__} - {e}")

    print(f'Done. Created {len(Voter.objects.all())} Voters.')




    




