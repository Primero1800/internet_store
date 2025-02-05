Демонстрация работы:

# https://www.primero1800.store/

Общая струтура интернет магазина:

<b>https://www.primero1800.store/posts/information/</b>

![block_content](https://github.com/user-attachments/assets/40600fb3-7433-48c1-b494-12f7c858900d)

Проект представляет собой готовый интернет магазин на <b>django</b>. <b>Fixtures</b> содержат информацию о:

1. Более сотни позиций товаров, 
2. Демонстрационных отзывов, заказов (доставленных, отмененных)
3. Зарегистрированных пользователях (в том числе из администрации сайта)
4. Более десятка сообщений на форуме от зарегистрированных пользователей

  В проекте применяются многочисленные <b>ajax-запросы</b> для динамического обновления контента при пагинации, фильтрации, сортировке, добавления товаров в корзину, списки избранного и сравнения, обновления контента при удалении позиций из списков и отзывов. 
Имеется дополнительная возможность использовать для интерфейса английский язык. 

  Регистрация пользователей осуществляется по <b>электронному адресу</b> с отправлением ссылки для активации аккаунта. 

  Имеется возможность <b>восстановления доступа</b> при утрате пароля.

  Добавление товаров <b>в корзину</b> и оформление заказов возможны как <b>для аутентифицированных пользователей</b>, так и <b>для анонимов</b>.

  При аутентификации анонима имеются две возможные настройки <b>поведения его корзины</b> (дополнительную информацию смотри во вложенном файле <b>INFO</b>).

  <b>Оповещение</b> администрации о изменениях в заказе, на форму и отзывах (различные варианты настройки) осуществляется посредством <b>телеграм-бота</b>.

  Работать с заказами, просматривать информацию о движении позиции можно как с помощью <b>специального инструментария сайта</b>, доступного только
для персонала, так посредством <b>панели управления /admin</b> или с помощью <b>API</b> (смотри во вложении <b>API_INFO</b>)

  С общей структурой интернет-магазина можно ознакомится по ссылке: 
	
 <b>https://primero1800.pythonanywhere.com/posts/information/</b>
	


# РУКОВОДСТВО ПО УСТАНОВКЕ И НАСТРОЙКЕ:

1. Клонируйте репозиторий:

	    https://github.com/Primero1800/internet_store.git
	
	    cd ElementarnoStore
    

Или скачайте исходный код репозитория в zip-архиве и распакуйте.



2. Создайте и активируйте виртуальное окружение:

	    python3 -m venv venv
	    source venv/bin/activate
    
3. Установите необходимые зависимости:

    	pip install -r requirements.txt
    
4. Войдите во внутреннюю папку проекта, сделайте миграции и загрузите подготовленные данные в бд:

	    cd mine_shop
	    python manage.py makemigrations
	    python manage.py migrate
	    python manage.py loaddata fixtures/data.json

5. (Опционально) В проекте используется собственная модель пользователя с аутентификацией по email и необязательным именем пользователя.
В подготовленном файле data.json уже имеются заранее созданные superuser. По умолчанию - (email: admin@admin.com, password: 12345678).
Для просмотра информации и создания собственных superuser необходимо запустить сеанс оболочки <b>python manage.py shell</b>.
   
    <b>superuser</b>r - функция, выводит список уже зарегистрированных superuser
   
    <b>defaultsuperuser</b> - функция, восстанавливает первоначального superuser

   (email: admin@admin.com, password: 12345678)
   
    <b>createsuperuser</b> - функция создания нового superuser:

	    python manage.py shell
	   
			from users.models import superuser, defaultsuperuser, createsuperuser
			superuser()
			defaultsuperuser()
   			createsuperuser ()

7. Запускаем сервер. (ВАЖНО!) В стандартных настройках приложения используется redis для кеширования.
    Если у Вас redis-server не установлен, по каким-либо причинам не желаете устанавливать или использовать установленный,
    воспользуйтесь docker.
    Файл docker-compose.yaml лежит в корневой директории проекта.
        
        cd ..
        docker-compose up --build   
        
        или

    	python manage.py runserver
    
8. Переходим:
    
    На сайт магазина: вводим в браузере http://127.0.0.1:8000/
   
    В панель администратора: вводим в браузере http://127.0.0.1:8000/admin/
   
      
9. (ВАЖНО) Детальные настройки сайта смотрим во вложенном файле <b>INFO</b>

	ОБРАТИТЕ ВНИМАНИЕ:
			для полноценной работы сайта, включающей отправку сообщений посредством
			электронной почты при регистрации нового пользователя или восстановления аккаунта
   			необходимо в файле .env ввести реквизиты своего почтового ящика, настроенного для работы
   			с smtp сервером.
   			для отправки уведомлений посредством телеграм-бота (при изменениях в статусе заказов, появлении
   			отзывов, оценок или постов на форуме) необходимы собственные настройки телеграм-бота в файле .env
            Переименуйте .env_template. на .env и добавьте в него свои настройки smtp и telegram_bot

11. (Опционально) Для работы с <b>API</b> пользуемся вкладкой <b>API</b> в верхнем меню на любой странице проекта.


<b>Фрагмент стартовой страницы:</b>

![index](https://github.com/user-attachments/assets/b437fee8-9140-407a-a780-aefcf9bc2a7b)

<b>Фрагмент страницы форума:</b>

![forum](https://github.com/user-attachments/assets/cd6409d2-43c8-42d6-a2de-be0bb3dc2ebe)

<b>Выпадающее меню корзины:</b>

![cart_dropdown](https://github.com/user-attachments/assets/f7e7fcdd-5b12-443e-bfb3-7c81693184f4)

