import click
from sayhello import app, db
from sayhello.models import Message

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    '''Initialize the database.'''
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop all tables.')
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages, default is 20.')
def forge(count):
    '''Generate fake messages.'''
    from faker import Faker

    db.drop_all()
    db.create_all()

    fake = Faker('zh_CN')
    click.echo('Working...')

    my_word_list = [
        '何日请缨提锐旅，一鞭直渡清河洛。',
        '杜鹃再拜忧天泪，精卫无穷填海心。',
        '半亩方塘一鉴开，天光云影共徘徊。',
        '大漠风尘日色昏，红旗半卷出辕门。',
        '金鞍玉勒寻芳客，未信我庐别有春。',
        '不知天上宫阙，今夕是何年。',
        '十年一觉扬州梦，赢得青楼薄幸名。',
        '一年春又尽，倚杖对斜晖。',
        '欲系青春，少住春还去。',
        '桃李务青春，谁能贯白日。'
    ]

    for i in range(count):
        message = Message(
            name=fake.name(),
            body=fake.sentence(ext_word_list=my_word_list),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(message)
    
    db.session.commit()
    click.echo('Create %d fake messages' % count)
