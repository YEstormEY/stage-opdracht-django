import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import CitySelectPage from "../components/CitySelectPage";

// Mock cities array used for testing.
const cities = [
  { code: "NYC", name: "New York City" },
  { code: "LA", name: "Los Angeles" },
  { code: "SF", name: "San Francisco" },
];

describe("CitySelectPage", () => {
  test("renders header, label and input", () => {
    // Render the CitySelectPage component with mock cities and no error.
    render(<CitySelectPage cities={cities} error={null} onSelectCity={() => {}}/>);

    // Assert that the header text "Select a City" is in the document.
    expect(screen.getByText("Select a City")).toBeInTheDocument();

    // Assert that the label text "Type a city name:" is rendered.
    expect(screen.getByText("Type a city name:")).toBeInTheDocument();

    // Assert that the input element with the expected placeholder is rendered.
    expect(screen.getByPlaceholderText("Search for a city...")).toBeInTheDocument();
  });

  test("displays an error message when error prop is provided", () => {
    // Define the expected error message.
    const errorMessage = "Failed to load cities!";
    // Render the component with an error passed to the error prop.
    render(<CitySelectPage cities={cities} error={errorMessage} onSelectCity={() => {}} />);

    // Assert that the provided error message is visible on the screen.
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  test("filters cities based on search input", () => {
    // Render the component with the mock cities and without an error.
    render(<CitySelectPage cities={cities} error={null} onSelectCity={() => {}} />);

    // Select the input element by its placeholder.
    const input = screen.getByPlaceholderText("Search for a city...");

    // Simulate typing "new" into the input field.
    fireEvent.change(input, { target: { value: "new" } });

    // Expect the suggestion "New York City" to appear in the list.
    expect(screen.getByText("New York City")).toBeInTheDocument();

    // Since the user typed "new", suggestions for "Los Angeles" and "San Francisco" should not be visible.
    expect(screen.queryByText("Los Angeles")).toBeNull();
    expect(screen.queryByText("San Francisco")).toBeNull();
  });

  test("clicking on a suggestion calls onSelectCity and updates input", () => {
    // Create a mock function to simulate the onSelectCity callback.
    const mockSelectCity = jest.fn();
    // Render the component with the mock onSelectCity callback.
    render(<CitySelectPage cities={cities} error={null} onSelectCity={mockSelectCity} />);

    // Select the input element.
    const input = screen.getByPlaceholderText("Search for a city...");

    // Simulate typing "los" to filter the list and match "Los Angeles".
    fireEvent.change(input, { target: { value: "los" } });

    // Ensure that the suggestion for "Los Angeles" appears.
    const suggestion = screen.getByText("Los Angeles");
    expect(suggestion).toBeInTheDocument();

    // Simulate a click on the "Los Angeles" suggestion.
    fireEvent.click(suggestion);

    // The mock onSelectCity function should be called with the city code "LA".
    expect(mockSelectCity).toHaveBeenCalledWith("LA");

    // The input field should be updated to display "Los Angeles" after the suggestion is clicked.
    expect(input.value).toBe("Los Angeles");
  });
});
