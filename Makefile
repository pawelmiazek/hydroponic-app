messages:
	docker exec -i hydroponic-django django-admin makemessages -l pl --ignore=__pypackages__


compile:
	docker exec -i hydroponic-django django-admin compilemessages -l pl --ignore=__pypackages__


test:
	docker exec -i hydroponic-django pytest .


shell:
	docker exec -it hydroponic-django bash
