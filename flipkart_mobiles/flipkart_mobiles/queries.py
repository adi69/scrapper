create_table = '''
    create table product_basic (
    name text,
    link text primary key,
    rating real,
    total_reviews integer,
    out_of_stock_status integer)'''

create_table_product = '''
    create table product (
    product text,
    seller text,
    selling_price real)'''
