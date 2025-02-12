import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import App from "../App";

// Sample city data returned by the mocked fetch for cities
const mockCities = [
  { code: "NYC", name: "New York City" },
  { code: "LA", name: "Los Angeles" },
  { code: "SF", name: "San Francisco" }
];

// Preserve the original global.fetch to restore later
const originalFetch = global.fetch;

describe("App Component Integration Tests", () => {
  beforeEach(() => {
    // Mock global.fetch to simulate API responses
    global.fetch = jest.fn((url) => {
      // If the URL requests cities, return mockCities
      if (url.includes("hotels/api/cities")) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockCities)
        });
      }
      // For other fetch calls such as fetching hotels, simulate an error response.
      return Promise.resolve({
        ok: false,
        json: () => Promise.reject(new Error("Error fetching hotels"))
      });
    });
  });

  afterEach(() => {
    // Restore original fetch and clear mocks
    global.fetch = originalFetch;
    jest.clearAllMocks();
  });

  test("renders CitySelectPage with header text", async () => {
    render(<App />);
    // Wait for the CitySelectPage header to appear
    await waitFor(() => {
      expect(screen.getByText("Select a City")).toBeInTheDocument();
    });
  });

  test("navigates to HotelsPage when a city is selected", async () => {
    render(<App />);
    // Wait for the city selection page to appear
    await waitFor(() => {
      expect(screen.getByText("Select a City")).toBeInTheDocument();
    });

    // Get the input field and simulate typing (using its placeholder)
    const input = screen.getByPlaceholderText("Search for a city...");
    fireEvent.change(input, { target: { value: "new" } });

    // Wait for the "New York City" suggestion to appear
    await waitFor(() => {
      expect(screen.getByText("New York City")).toBeInTheDocument();
    });

    // Simulate clicking on "New York City"
    fireEvent.click(screen.getByText("New York City"));

    // After selection, the HotelsPage should display a header with the selected city
    await waitFor(() => {
      expect(screen.getByText(/Hotels in New York City/)).toBeInTheDocument();
    });
  });

  test("returns to CitySelectPage when back button is clicked", async () => {
    render(<App />);
    // Verify CitySelectPage is displayed
    await waitFor(() => {
      expect(screen.getByText("Select a City")).toBeInTheDocument();
    });

    // Simulate selecting a city
    const input = screen.getByPlaceholderText("Search for a city...");
    fireEvent.change(input, { target: { value: "new" } });
    await waitFor(() => {
      expect(screen.getByText("New York City")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByText("New York City"));

    // Ensure HotelsPage is rendered
    await waitFor(() => {
      expect(screen.getByText(/Hotels in New York City/)).toBeInTheDocument();
    });

    // Simulate clicking the back button (assuming the button has text "← Back")
    fireEvent.click(screen.getByText("← Back"));

    // Verify that the CitySelectPage is shown again
    await waitFor(() => {
      expect(screen.getByText("Select a City")).toBeInTheDocument();
    });
  });
});
