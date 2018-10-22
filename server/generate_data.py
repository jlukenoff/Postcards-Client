from faker import Faker
from app import Users, db, lob

fake = Faker('en_US')

for i in range(100):
	# create listing in lob address book
	user = lob.Address.create(
		name=fake.name(),
		description=fake.sentence(),
		metadata={
			'group': 'Members'
		},
		address_line1=fake.street_address(),
		address_city=fake.city(),
		address_state=fake.state(),
		address_country='US',
		address_zip=fake.zipcode(),
		phone=fake.phone_number(),
		email=fake.free_email()
	)

	# set created date to simulate users creating accounts throughout the year
	created_date = fake.date_this_year(before_today=True, after_today=False)

	# create a record from sqlalchemy model
	user_record = Users(
		id=user.id,
		company=user.company,
		date_created=created_date,
		description=user.description,
		email=user.email,
		name=user.name,
		phone=user.phone,
		address_city=user.address_city,
		address_country=user.address_country,
		address_line1=user.address_line1,
		address_line2=user.address_line2,
		address_state=user.address_state,
		address_zip=user.address_zip,
		anniversary=str(created_date.month) + '-' + str(created_date.day),
		password=fake.md5()
	)
	# add model to db session
	db.session.add(user_record)
# add all records to db session
db.session.commit()
