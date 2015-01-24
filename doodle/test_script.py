#encoding: utf-8

import boto.dynamodb2
from boto.dynamodb2.table import Table

def main():

	conn = boto.dynamodb2.connect_to_region(
				'us-west-2',
				aws_access_key_id='AKIAJFBBXT6CLH4UHOLQ',
				aws_secret_access_key='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'
				)

	Test_Table = Table('Test_Table', connection=conn)

	result = Test_Table.query(Timestamp__eq='timestamp1',index='Timestamp-index')

	for res in result:
		print(res['Timestamp'])

if __name__ == "__main__": main()
