from app import lob

address_list = lob.Address.list(limit=100)
while len(address_list.data) > 0:

	for address in address_list.data:
		print('Deleting:' + address.id)
		lob.Address.delete(address.id)

	address_list = lob.Address.list(limit=100)