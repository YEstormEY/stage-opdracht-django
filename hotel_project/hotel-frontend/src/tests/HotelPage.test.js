import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import HotelsPage from "../components/HotelsPage";

// Define a sample selected city for testing
const selectedCity = { code: "NYC", name: "New York City" };

describe("HotelsPage", () => {
  // Save the original fetch so we can restore it after each test.
  const originalFetch = global.fetch;

  afterEach(() => {
    // Restore the global fetch function after each test
    global.fetch = originalFetch;
    // Clear all mock data to avoid test interference
    jest.clearAllMocks();
  });

  test("renders header and back button and handles state updates without act warning", async () => {
    // Mock fetch to simulate a successful API call that returns an empty hotel list.
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([]),
      })
    );

    // Create a mock function for the onBack callback
    const mockOnBack = jest.fn();
    // Render the HotelsPage component with the selected city and onBack callback
    render(<HotelsPage selectedCity={selectedCity} onBack={mockOnBack} />);

    // Use waitFor to ensure asynchronous state updates from the API call complete
    await waitFor(() => {
      // Verify that the header containing the selected city's name is rendered.
      expect(screen.getByText(`Hotels in ${selectedCity.name}`)).toBeInTheDocument();
    });

    // Verify that the "Back" button is rendered by checking its text content.
    expect(screen.getByText("← Back")).toBeInTheDocument();
  });

  test("Shows a loading message while fetching hotels", async () => {
    // Mock fetch to return a never-resolving promise to simulate a loading state.
    global.fetch = jest.fn(() => new Promise(() => {}));

    const mockOnBack = jest.fn();
    // Render the component
    render(<HotelsPage selectedCity={selectedCity} onBack={mockOnBack} />);

    // Immediately check for the loading message.
    // The regex allows matching "Loading hotels..." exactly.
    expect(screen.getByText(/Loading hotels\.\.\./)).toBeInTheDocument();
  });

  test("displays an error message when fetch fails", async () => {
    // Mock fetch to simulate a failed API call (response.ok is false)
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
      })
    );

    const mockOnBack = jest.fn();
    // Render the component
    render(<HotelsPage selectedCity={selectedCity} onBack={mockOnBack} />);

    // Wait for the error message to be rendered.
    // The regex matcher is flexible in case the text is split across elements.
    await waitFor(() => {
      expect(screen.getByText(/Failed to load hotels\./)).toBeInTheDocument();
    });
  });

  test("renders hotels when fetch is successful", async () => {
    // Create an array of hotel objects to simulate a successful API response.
    const hotels = [
      { city: "AMS", code: "AMS01", name: "Hotel 1" },
      { city: "AMS", code: "AMS02", name: "Hotel 2" },
    ];
    // Mock fetch to return the hotels data.
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(hotels),
      })
    );

    const mockOnBack = jest.fn();
    // Render the component
    render(<HotelsPage selectedCity={selectedCity} onBack={mockOnBack} />);

    // Wait for each hotel name to be rendered in the DOM.
    await waitFor(() => {
      expect(screen.getByText("Hotel 1")).toBeInTheDocument();
    });
    await waitFor(() => {
      expect(screen.getByText("Hotel 2")).toBeInTheDocument();
    });
  });

  test("renders no hotels message when there are no hotels", async () => {
    // Mock fetch to return an empty array of hotels for a successful call.
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([]),
      })
    );

    const mockOnBack = jest.fn();
    // Render the component
    render(<HotelsPage selectedCity={selectedCity} onBack={mockOnBack} />);

    // Wait until the "no hotels" message appears.
    await waitFor(() => {
      expect(screen.getByText("No hotels found in this city.")).toBeInTheDocument();
    });
  });

  test("calls onBack callback when back button is clicked", async () => {
    // Mock fetch to simulate a successful API call that returns an empty hotel list.
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([]),
      })
    );

    const mockOnBack = jest.fn();
    // Render the HotelsPage component.
    render(<HotelsPage selectedCity={selectedCity} onBack={mockOnBack} />);

    // Wait until the header is rendered to ensure the component state is up-to-date.
    await waitFor(() => {
      expect(screen.getByText(`Hotels in ${selectedCity.name}`)).toBeInTheDocument();
    });

    // Find the back button using its visible text.
    const backButton = screen.getByText("← Back");
    // Simulate a user click on the back button.
    fireEvent.click(backButton);
    // Verify that the onBack callback has been called after the click.
    expect(mockOnBack).toHaveBeenCalled();
  });
});
