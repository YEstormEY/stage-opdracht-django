import react from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import CitySelectPage from "../components/CitySelectPage";

// Mock cities for testing
const cities = [
    { code: "NYC", name: "New York City" },
    { code: "LA", name: "Los Angeles" },
    { code: "SF", name: "San Francisco" },
]

describe("CitySelectPage", () => {
    test("renders header, label and input", () => {
        render(<CitySelectPage cities={cities} error={null} onSelectCity={() => {}}/>);

        //check for header text
        expect(screen.getByText("Select a City")).toBeInTheDocument();

        //check for label text
        expect(screen.getByText("Type a city name:")).toBeInTheDocument();

        //check for input element
        expect(screen.getByPlaceholderText("Search for a city...")).toBeInTheDocument();
    })

    test("displays an error message when error prop is provided", () => {
        // Use the expected error message
        const errorMessage = "Failed to load cities!";
        render(<CitySelectPage cities={cities} error={errorMessage} onSelectCity={() => {}} />);
    
        // Verify that the error message is rendered on screen.
        expect(screen.getByText(errorMessage)).toBeInTheDocument();
      });

    test("filters cities based on search input", () => {
        render(<CitySelectPage cities={cities} error={null} onSelectCity={() => {}} />);
        
        const input = screen.getByPlaceholderText("Search for a city...");
        
        // Type "new" should filter and show only "New York City"
        fireEvent.change(input, { target: { value: "new" } });
        
        // Expect New York City to appear in the suggestion list
        expect(screen.getByText("New York City")).toBeInTheDocument();
        
        // Suggestions for Los Angeles and San Francisco should not be visible
        expect(screen.queryByText("Los Angeles")).toBeNull();
        expect(screen.queryByText("San Francisco")).toBeNull();
      });

      test("clicking on a suggestion calls onSelectCity and updates input", () => {
        const mockSelectCity = jest.fn();
        render(<CitySelectPage cities={cities} error={null} onSelectCity={mockSelectCity} />);
        
        const input = screen.getByPlaceholderText("Search for a city...");
        
        // Type "los" to filter and match "Los Angeles"
        fireEvent.change(input, { target: { value: "los" } });
        
        // Verify that suggestion appears
        const suggestion = screen.getByText("Los Angeles");
        expect(suggestion).toBeInTheDocument();
        
        // Click the suggestion
        fireEvent.click(suggestion);
        
        // Verify that onSelectCity callback is called with "LA"
        expect(mockSelectCity).toHaveBeenCalledWith("LA");
        
        // The input field should update to the clicked city's name ("Los Angeles")
        expect(input.value).toBe("Los Angeles");
      });
});

