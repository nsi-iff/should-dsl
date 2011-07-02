Basic Usage
===========

.. toctree::
    :maxdepth: 2
    :hidden:

    available_matchers
    predicate_matchers
    custom_matchers
    contributing
    license


The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using an **"almost"** natural language (limited by some Python language's constraints).

In order to use this DSL, you need to import ``should`` and ``should_not`` objects from ``should_dsl`` module.

cards_game_spec.py::

    import unittest
    from should_dsl import should, should_not
    from cards_game import Player, Card


    class CardsGameExamples(unittest.TestCase):

      def setUp(self):
        self.player = Player('John Doe')

      def test_player_has_initial_number_of_cards(self):
        self.player |should| have(11).cards

      def test_player_has_a_name(self):
        self.player.name |should| equal_to('John Doe')

      def test_discard_card(self):
        card = Card('Q', 'spades')
        self.player.discard(card)
        self.player.hand |should_not| contain(card)


    if __name__ == '__main__':
        unittest.main()


.. code-block:: bash

    $ python cards_game_spec.py  -v
    test_discard_card (__main__.CardsGameExamples) ... ok
    test_player_has_initial_number_of_cards (__main__.CardsGameExamples) ... ok
    test_player_has_a_name (__main__.CardsGameExamples) ... ok

    ----------------------------------------------------------------------
    Ran 3 tests in 0.002s

    OK


Documentation
=============

`Should-DSL Matchers <available_matchers.html>`_: check all available matchers

`Predicate Matchers <predicate_matchers.html>`_: predicate matchers are the matchers that work with boolean methods and attributes, giving users more freedom to write more readable specifications.

`Custom Matchers <custom_matchers.html>`_: extending Should-DSL with custom matchers is very easy. It is possible to add matchers through functions and classes, for simple and complex behaviors.

`Contributing <contributing.html>`_: see how you can contribute to Should-DSL development

`License <license.html>`_: MIT License


Installation
------------

Should-DSL can be installed through PyPI, using :command:`pip` or :command:`easy_install`.

.. code-block:: bash

    $ pip install should-dsl
    # maybe you need to run it as sudo

