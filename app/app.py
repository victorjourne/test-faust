import faust
from faust.web import Request, Response, View

import os

app = faust.App(
    'test',
    debug=False,
    broker=os.getenv("FAUST_BROKER_URL"),
    topic_partitions=int(os.getenv("NB_PARTITIONS", 1)),
    value_serializer='json'
)

table = app.Table('info', key_type=str, value_type=str)


@app.agent(key_type=str, value_type=str, concurrency=1)
async def write_info(stream):
    """Write in table without concurrency
    """
    async for key, value in stream.items():
        table[key] = value
        yield

@app.page('/info/{key}/')
@app.table_route(table=table, match_info='key')
async def get_info(web, request: Request, key) -> Response:
    try:
        value = table[key]
        return web.json(value)
    except KeyError:
        raise View.NotFound(f"Cannot find this symbol among [{table.keys()}]")


@app.page("/info")
class info(View):
        
    async def get(self, request: Request) -> Response:
        # Downloads infos
        return self.json({symbol: value for symbol, value in table.items()})

    async def post(self, request: Request) -> Response:
        json_data = await request.json()
        await write_info.cast(key=json_data['key'], value=json_data['value'])
        return self.json({"message": f"Post {json_data['key']}"})
