from sqlalchemy import create_engine
from sqlalchemy import text
from celery import Celery
from celery.schedules import crontab
from helpers.item import Item
from helpers.amazon import Amazon


engine = create_engine('postgresql+psycopg2://kiero:*1q2w3e*@51.222.103.209:53092/kierodb')

app = Celery('task', broker='pyamqp://guest@localhost//')


app.conf.beat_schedule = {
    'run_every_ten_sec': {
        'task': 'tasks.init_process',
        'schedule': 300.0
    }
}

amazon = Amazon()
# def write2file(product, item, status):
    # with open('output/'+product.asin, 'w') as f:
        # f.writelines(f'{product.id},{product.asin},{product.url},{item.title},{item.price},{status}\n')
    # return True
    
def write2db(product, item, status):
    sql = text('insert into scraper values(:id, :asin, :title, :status, :price, :old_price, :description)')
    with engine.connect() as connection:
        connection.execute(sql, id= product.id, asin= product.asin, title= item.title, 
            old_price= item.price['old_price'], price= item.price['price'], status= status, description=item.description)
        

@app.task
def init_process():
    with open('asins', 'r') as file:
        for data in file.readlines():
            scrap_product.apply_async((data,))

@app.task
def scrap_product(data):
    #print(data)
    product = amazon.build_url(data)
    soup = amazon.get(product)
    item = Item(soup)
    status = 1 if item.price != 0 else 0
    # write2file(product, item, status)
    write2db(product, item, status)
    print(product.asin, item.price['old_price'],item.price['price'])