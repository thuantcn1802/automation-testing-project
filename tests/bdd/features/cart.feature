Feature: Shopping cart totals
  As a shopper
  I want the cart to calculate prices for my selected quantities
  So that I know how much I will pay

  Background:
    Given I am on the home page

  Scenario Outline: Adding a product calculates the correct cart total
    When I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I view my cart
    Then the cart contains "<product>" with quantity <quantity>
    And the line price equals the unit price multiplied by <quantity>
    And the cart total equals the sum of the line prices

    Examples:
      | product            | quantity |
      | Combination Pliers | 1        |
      | Claw Hammer        | 3        |
