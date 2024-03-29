from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pereval.models import Pereval, Coords, Users, Images
from pereval.serializers import PerevalSerializer, PerevalDetailSerializer


class SubmitDataApiTestCase(APITestCase):
    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            beauty_title='пер.',
            title='Перевал Чике-Таман',
            other_titles='Чике-Таман',
            connect='Семинский перевал',
            add_time='2023-08-30 16:30:32.859243+00',
            status='new',
            level='winter-2A',
            coordinates=Coords.objects.create(
                latitude=1.0,
                longitude=3.0,
                height=4
            ),
            user=Users.objects.create(
                first_name='Иван',
                last_name='Иванов',
                patronymic='Иванович',
                email='ivan@gmail.com',
                phone='+79182564689'
            ),
            images=Images.objects.create(
                title_1='Перевал Чике-Таман',
                image_1='https://www.google.com/url?sa=i&url=https%3A%2F%2Fvisit',
                title_2='',
                image_2='',
                title_3='',
                image_3=''
            )
        )

        self.pereval_2 = Pereval.objects.create(
            beauty_title='Пер.',
            title='Перевал Teodulpass',
            other_titles='Теодуль, Teodulo',
            connect='ледник Теодуль и долину реки Мармор',
            add_time='2023-07-20 16:30:32.859243+00',
            status='new',
            level='winter-1A',
            coordinates=Coords.objects.create(
                latitude=1.0,
                longitude=2.0,
                height=3
            ),
            user=Users.objects.create(
                first_name='Василий',
                last_name='Васильев',
                patronymic='Васильевич',
                email='vasyl60@example.com',
                phone='+70123456789'
            ),
            images=Images.objects.create(
                title_1='Перевал Teodulpass-1',
                image_1='https://upload.wikimedia.org/wikipedia/commons/e/ef/Colle_del_Teodulo_001.jpg',
                title_2='Перевал Teodulpass-2',
                image_2='https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Rif-theodulo.jpg/800px-Rif'
                        '-theodulo.jpg',
                title_3='',
                image_3=''
            )
        )

    def test_get_submitdata(self):
        response = self.client.get(reverse('submitData'))
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2, ], many=True).data
        self.assertEquals(serializer_data, response.data['results'], msg='Ошибка! Данные не соответствуют')
        self.assertEquals(len(serializer_data), 2, msg='Ошибка! Не соответствует длина списка'),
        self.assertEquals(status.HTTP_200_OK, response.status_code, msg='Ошибка! Статус не соответствует')

    def test_get_submitdetaildata(self):
        response = self.client.get(reverse('submitDetailData', args=(self.pereval_1.id,)))
        serializer_data = PerevalDetailSerializer(self.pereval_1).data
        self.assertEquals(serializer_data, response.data, msg='Ошибка! Данные не соответствуют')
        self.assertEquals(status.HTTP_200_OK, response.status_code, msg='Ошибка! Статус не соответствует')


class SubmitDataPostAPITests(APITestCase):
    def setUp(self):
        self.pereval_3 = {
            'beauty_title': 'Test beauty_title',
            'title': 'Test title',
            'other_titles': 'Test other_titles',
            'connect': 'Test connect',
            'add_time': '2023-07-20 16:30:32.859243+00',
            'status': 'new',
            'level': 'winter-1A',
            'coordinates': {'latitude': 1.0,
                            'longitude': 2.0,
                            'height': 3
                            },
            'user': {'first_name': 'Test first name',
                     'last_name': 'Test last name',
                     'patronymic': 'Test patronomic',
                     'email': 'test@example.com',
                     'phone': '+70123456789'
                     },
            'images': {'title_1': 'Test title-1',
                       'image_1': '',
                       'title_2': 'Test title-2',
                       'image_2': '',
                       'title_3': 'Test title-3',
                       'image_3': ''
                       }
        }

    def test_post_submitData(self):
        response = self.client.post(reverse('submitData'), self.pereval_3, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg='Ошибка: Статус код не соответствует')
        self.assertEqual(Pereval.objects.count(), 1, msg='Ошибка: Количество не соответствует')
        self.assertEqual(Pereval.objects.get().beauty_title, 'Test beauty_title', msg='Ошибка: Данные не соответствуют')
        self.assertEqual(Users.objects.get().first_name, 'Test first name', msg='Ошибка: Данные не соответствуют')
        self.assertEqual(Coords.objects.get().latitude, 1.0, msg='Ошибка: Данные не соответствуют')
