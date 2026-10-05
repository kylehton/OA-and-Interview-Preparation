import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from mini_template import DictTemplateLoader, TemplateRenderer


def renderer(templates):
    return TemplateRenderer(DictTemplateLoader(templates))


def test_plain_text_and_basic_variable():
    result = renderer({"hello.tpl": "Hello {{ name }}!"}).render(
        "hello.tpl", {"name": "Ada"}
    )
    assert result == "Hello Ada!"


def test_escaped_variable_handles_markup():
    result = renderer({"x.tpl": "{{ value }}"}).render(
        "x.tpl", {"value": "<strong>A&B</strong>"}
    )
    assert result == "&lt;strong&gt;A&amp;B&lt;/strong&gt;"


def test_escaped_variable_handles_attribute_quotes():
    result = renderer({"x.tpl": '<div title="{{ value }}">'}).render(
        "x.tpl", {"value": 'say "hello" & \'bye\''}
    )
    assert result == (
        '<div title="say &quot;hello&quot; &amp; &#x27;bye&#x27;">'
    )


def test_raw_variable_is_not_escaped_or_partially_tokenized():
    result = renderer({"x.tpl": "before {{{ html }}} after"}).render(
        "x.tpl", {"html": "<b>safe</b>"}
    )
    assert result == "before <b>safe</b> after"


def test_dotted_lookup_and_missing_value():
    result = renderer({"x.tpl": "{{ customer.name }}:{{ customer.missing }}"}).render(
        "x.tpl", {"customer": {"name": "Lin"}}
    )
    assert result == "Lin:"


def test_static_include():
    result = renderer(
        {"page.tpl": 'A{% include "footer.tpl" %}', "footer.tpl": "Z"}
    ).render("page.tpl", {})
    assert result == "AZ"


def test_include_inherits_parent_context():
    result = renderer(
        {
            "page.tpl": 'Hi {% include "name.tpl" %}',
            "name.tpl": "{{ customer.name }}",
        }
    ).render("page.tpl", {"customer": {"name": "Sam"}})
    assert result == "Hi Sam"


def test_cache_keys_use_complete_template_path():
    view = renderer(
        {
            "emails/base.tpl": "Email {{ name }}",
            "admin/base.tpl": "Admin {{ name }}",
        }
    )
    assert view.render("emails/base.tpl", {"name": "A"}) == "Email A"
    assert view.render("admin/base.tpl", {"name": "B"}) == "Admin B"

