import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / "main.py"


class Section:
    def __init__(self, title, sections):
        self.title = title
        self.sections = sections


class WikiPage:
    def __init__(self, sections):
        self.text = "<html></html>"
        self.sections = sections


def load_scraper_module(page_fixtures):
    wikipediaapi = types.ModuleType("wikipediaapi")
    wikipediaapi.ExtractFormat = types.SimpleNamespace(HTML="html")

    class FakeWikipedia:
        def __init__(self, language, extract_format):
            self.language = language
            self.extract_format = extract_format

        def page(self, player):
            return page_fixtures[player]

    wikipediaapi.Wikipedia = FakeWikipedia
    pandas = types.ModuleType("pandas")
    requests = types.ModuleType("requests")
    urllib_request = types.ModuleType("urllib.request")
    bs4 = types.ModuleType("bs4")
    bs4.BeautifulSoup = lambda html, parser: (html, parser)
    modules = {
        "pandas": pandas,
        "requests": requests,
        "urllib.request": urllib_request,
        "bs4": bs4,
        "wikipediaapi": wikipediaapi,
    }
    spec = importlib.util.spec_from_file_location("football_player_main", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load scraper module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module


def make_sections(specification):
    return [
        Section(
            root_title,
            [
                Section(
                    child_title,
                    [Section(grandchild_title, []) for grandchild_title in grandchildren],
                )
                for child_title, grandchildren in children
            ],
        )
        for root_title, children in specification
    ]


def reference_titles(sections):
    """Independent flattening reference for the documented club-career output."""
    root_groups = [
        [
            section.title,
            *[
                title
                for child in section.sections
                for title in (
                    [child.title]
                    + [grandchild.title for grandchild in child.sections]
                )
            ],
        ]
        for section in sections
        if "Club career" in section.title
    ]
    titles = [title for group in root_groups for title in group]
    return "\n".join(titles) + ("\n" if titles else "")


def section_snapshot(sections):
    return tuple(
        (
            root.title,
            tuple(
                (child.title, tuple(grandchild.title for grandchild in child.sections))
                for child in root.sections
            ),
        )
        for root in sections
    )


class MyScraperReferenceTests(unittest.TestCase):
    def run_scraper(self, player, sections):
        original_sections = section_snapshot(sections)
        fixtures = {player: WikiPage(sections)}
        scraper_module = load_scraper_module(fixtures)
        scraper = scraper_module.myScraper(player)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = scraper.execute()
        self.assertEqual(scraper.player, player)
        self.assertEqual(section_snapshot(sections), original_sections)
        return result, output.getvalue()

    def assert_matches_reference(self, player, sections):
        expected = reference_titles(sections)
        actual_result, actual = self.run_scraper(player, sections)
        print(
            f"player={player!r}, expected_output={expected!r}, "
            f"actual_output={actual!r}, return={actual_result!r}"
        )
        self.assertIsNone(actual_result)
        self.assertEqual(actual, expected, f"expected={expected!r}; actual={actual!r}")

    def test_smallest_player_input_has_no_section_output(self):
        # main.py lines 11-18 establish a player-name input and load the page;
        # an empty section list is the smallest valid page fixture.
        player = "A"
        sections = []
        expected = ""
        actual_result, actual = self.run_scraper(player, sections)
        print(
            f"player={player!r}, sections={sections!r}, "
            f"expected_output={expected!r}, actual_output={actual!r}"
        )
        self.assertIsNone(actual_result)
        self.assertEqual(actual, expected, f"expected={expected!r}; actual={actual!r}")

    def test_non_club_section_child_is_excluded_minimal_counterexample(self):
        # README lines 25-26 limit retrieved output to club-career sections.
        # A non-club root with one child is the smallest counterexample.
        player = "Fixture Player"
        sections = make_sections([("Overview", [("Biography", [])])])
        expected = ""
        actual_result, actual = self.run_scraper(player, sections)
        print(
            f"minimal input={player!r}, expected_output={expected!r}, "
            f"actual_output={actual!r}"
        )
        self.assertIsNone(actual_result)
        self.assertEqual(actual, expected, f"expected={expected!r}; actual={actual!r}")

    def test_ordinary_player_and_club_career_section(self):
        # main.py lines 11-18 load the named player's page, and lines 20-35
        # traverse its section tree. Fixture content is deliberately local.
        player = "Lionel Messi"
        sections = make_sections(
            [
                ("Overview", [("Early life", [])]),
                (
                    "Club career",
                    [("Barcelona", ["2004–2021"]), ("Inter Miami", [])],
                ),
            ]
        )
        expected = "Club career\nBarcelona\n2004–2021\nInter Miami\n"
        actual_result, actual = self.run_scraper(player, sections)
        print(
            f"player={player!r}, expected_output={expected!r}, "
            f"actual_output={actual!r}"
        )
        self.assertIsNone(actual_result)
        self.assertEqual(actual, expected, f"expected={expected!r}; actual={actual!r}")

    def test_twenty_small_section_trees_match_independent_reference(self):
        # Section trees use the title/children shape consumed at main.py lines
        # 20-35. All fixtures contain list-valued sections as supplied by the
        # normal Wikipedia section API; each scraper gets fresh objects.
        cases = []
        for index in range(10):
            club_title = "Club career" if index % 2 == 0 else f"Other {index}"
            cases.append(
                [
                    (
                        club_title,
                        [
                            (
                                f"Club {index}",
                                [f"Season {index}"] if index % 3 == 0 else [],
                            )
                        ],
                    )
                ]
            )
            cases.append(
                [
                    (f"Other root {index}", [(f"Ignore {index}", [])]),
                    (
                        f"Club career {index}" if index % 2 else "Club career",
                        [
                            (
                                f"Team A {index}",
                                [f"Year A {index}", f"Year B {index}"],
                            ),
                            (f"Team B {index}", []),
                        ],
                    ),
                ]
            )

        self.assertEqual(len(cases), 20)
        for index, specification in enumerate(cases):
            with self.subTest(case=index, specification=specification):
                sections = make_sections(specification)
                self.assert_matches_reference(f"Fixture Player {index}", sections)


if __name__ == "__main__":
    unittest.main()
