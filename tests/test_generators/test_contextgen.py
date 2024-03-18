import pdb
import re
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml import LOCAL_TYPES_YAML_FILE, METAMODEL_NAMESPACE


def test_context(kitchen_sink_path):
    """json schema"""
    ContextGenerator(kitchen_sink_path).serialize()


def test_rdflib_string_handling():
    """
    Ensure that we don't make mistakes expecting rdflib stringlike-classes to behave
    like strings!

    Eg. :class:`rdflib.Namespace` inherits from ``str`` , but overrides the ``contains`` method
    """
    generated = ContextGenerator(LOCAL_TYPES_YAML_FILE).serialize(base=METAMODEL_NAMESPACE)
    assert not re.search(r"http:/[^/]", generated)
    assert not re.search(r"https:/[^/]", generated)


def test_model_field_usage(tmp_path):
    """
    When a field is allowed in both the generator instantiation and serialization method,
    use the instance field when the serialization arg isn't provided
    """
    generated = ContextGenerator(LOCAL_TYPES_YAML_FILE, base=METAMODEL_NAMESPACE).serialize()
    assert "@base" in generated

    output_path = tmp_path.with_suffix(".context.json")
    generated = ContextGenerator(LOCAL_TYPES_YAML_FILE, output=str(output_path)).serialize(base=METAMODEL_NAMESPACE)
    assert generated is None
    assert output_path.exists()
