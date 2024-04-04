from factory import Factory, Faker
from factory.fuzzy import FuzzyInteger, FuzzyText
from polyfactory import Use

from plants_api.plants.models import PlantCreate, PlantRead, Plant

from polyfactory.factories import BaseFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory


class PlantBaseFactory(Factory):
    class Meta:
        model = Plant

    latin_name = FuzzyText()

    min_germination_temp = FuzzyInteger(0, 40)
    max_germination_temp = FuzzyInteger(41, 85)

    min_soil_temp_transplant = FuzzyInteger(20, 60)
    max_soil_temp_transplant = FuzzyInteger(61, 100)

    common_names = []


class PlantFactory(PlantBaseFactory):
    class Meta:
        model = Plant

    pk = Faker("uuid4")


# class PlantFactory(BaseFactory[Plant]):
#     __model__ = Plant
#     __allow_none_optionals___ = False

#     name = Use(BaseFactory.__random__.choice, ["Ralph", "Roxy"])

# class PlantFactory(SQLAlchemyFactory[Plant]):
#     ...


class PlantCreateFactory(PlantBaseFactory):
    class Meta:
        model = PlantCreate

    pk = None


# class PlantCreateFactory(BaseFactory[PlantCreate]):
#     ...


class PlantReadFactory(PlantBaseFactory):
    class Meta:
        model = PlantRead

    pk = Faker("uuid4")


# class PlantReadFactory(BaseFactory[PlantRead]):
#     ...
