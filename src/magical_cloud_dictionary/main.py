import boto3


class Magic:
    def __init__(self, table: str) -> None:
        self.table = table

    def put(self, key: str, value) -> None:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table)
        # NOTE if you want to support floats add this probably, untested
        # x = json.loads(json.dumps(cartBefore), parse_float=Decimal)
        response = table.put_item(
            Item={
                "key": key,
                "value": value,
            }
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def get(self, key: str):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table)
        response = table.get_item(
            Key={
                "key": key,
            }
        )
        return response["Item"]["value"]
