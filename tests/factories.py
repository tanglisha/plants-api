import random

from factory import Factory
from factory import Faker
from factory import LazyAttribute
from factory import RelatedFactoryList
from factory import SelfAttribute
from factory import SubFactory
from factory.fuzzy import FuzzyInteger
from plants_api.plants.models import CommonName
from plants_api.plants.models import CommonNameCreate
from plants_api.plants.models import Plant
from plants_api.plants.models import PlantCreate
from plants_api.plants.models import PlantRead


class CommonNameBaseFactory(Factory):
    class Meta:  # type:ignore
        model = CommonName

    name = Faker("sentence", nb_words=3, variable_nb_words=True)
    plant_id = LazyAttribute(
        lambda o: SelfAttribute("plant.id") if o.plant else None,
    )
    plant = SubFactory(
        "tests.factories.PlantBaseFactory",
        _sa_instance_state="instance state from CommonNameBaseFactory",
    )


class CommonNameFactory(CommonNameBaseFactory):
    class Meta:  # type:ignore
        model = CommonName

    pk = Faker("uuid4")


class CommonNameCreateFactory(CommonNameBaseFactory):
    class Meta:  # type:ignore
        model = CommonNameCreate

    pk = None


class CommonNameReadFactory(Factory):
    class Meta:  # type:ignore
        model = CommonName

    name = Faker("sentence", nb_words=3, variable_nb_words=True)


class PlantBaseFactory(Factory):
    class Meta:  # type:ignore
        model = Plant

    latin_name = Faker("sentence", nb_words=3, variable_nb_words=True)

    min_germination_temp = FuzzyInteger(0, 40)
    max_germination_temp = FuzzyInteger(41, 85)

    min_soil_temp_transplant = FuzzyInteger(20, 60)
    max_soil_temp_transplant = FuzzyInteger(61, 100)


class PlantFactory(PlantBaseFactory):
    class Meta:  # type:ignore
        model = Plant

    pk = Faker("uuid4")

    common_names = RelatedFactoryList(
        factory="tests.factories.CommonNameFactory",
        factory_related_name="plant",
        # size=FuzzyInteger(0, 5).fuzz(),  # Try to be random for each instance
        size=random.randint(0, 5),
        _sa_instance_state="instance state from PlantFactory",
        plant_id="..pk",
    )


class PlantCreateFactory(PlantBaseFactory):
    class Meta:  # type:ignore
        model = PlantCreate

    pk = None

    common_names = RelatedFactoryList(
        factory="tests.factories.CommonNameCreateFactory",
        factory_related_name="plant",
        size=random.randint(0, 5),
        _sa_instance_state="instance state from PlantFactory",
        plant_id="..pk",
    )


class PlantReadFactory(PlantFactory):
    class Meta:  # type:ignore
        model = PlantRead

    pk = Faker("uuid4")
