from factory import Factory
from factory import Faker
from factory import RelatedFactoryList
from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyInteger
from plants_api.plants.models import CommonName
from plants_api.plants.models import CommonNameCreate
from plants_api.plants.models import Plant
from plants_api.plants.models import PlantCreate
from plants_api.plants.models import PlantRead


class CommonNameBaseFactory(SQLAlchemyModelFactory):
    class Meta:  # type:ignore
        model = CommonName

    name = Faker("sentence", nb_words=3, variable_nb_words=True)
    plant = SubFactory(
        "tests.factories.PlantBaseFactory",
        _sa_instance_state="name",
    )


class CommonNameFactory(CommonNameBaseFactory):
    class Meta:  # type:ignore
        model = CommonName

    pk = Faker("uuid4")


class CommonNameCreateFactory(CommonNameBaseFactory):
    class Meta:  # type:ignore
        model = CommonNameCreate

    pk = None


class CommonNameReadFactory(CommonNameBaseFactory):
    class Meta:  # type:ignore
        model = CommonName

    pk = Faker("uuid4")


class PlantBaseFactory(Factory):
    class Meta:  # type:ignore
        model = Plant

    latin_name = Faker("sentence", nb_words=3, variable_nb_words=True)

    min_germination_temp = FuzzyInteger(0, 40)
    max_germination_temp = FuzzyInteger(41, 85)

    min_soil_temp_transplant = FuzzyInteger(20, 60)
    max_soil_temp_transplant = FuzzyInteger(61, 100)

    common_names = RelatedFactoryList(
        factory="tests.factories.CommonNameFactory",
        factory_related_name="plant",
        size=2,
        _sa_instance_state="plant",
    )


class PlantFactory(PlantBaseFactory):
    class Meta:  # type:ignore
        model = Plant

    pk = Faker("uuid4")


class PlantCreateFactory(PlantBaseFactory):
    class Meta:  # type:ignore
        model = PlantCreate

    pk = None


class PlantReadFactory(PlantBaseFactory):
    class Meta:  # type:ignore
        model = PlantRead

    pk = Faker("uuid4")
