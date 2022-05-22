from seeding.seeding import BaseSeeding

from mainapp.models import News


class Seeding(BaseSeeding):

    def seeding(self):
        data_list = []
        for i in range(50):
            data_list.append(News(
                title=f'Some new news #{i}',
                preambule=f'Preambule of some new news #{i}',
                body=f'Body of some new news #{i}'
            ))
        News.objects.bulk_create(data_list)

    def rollback(self):
        """ Remove seeded data from project  """
        pass
