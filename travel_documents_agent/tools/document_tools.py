"""Document generation tools for creating visual travel documents."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader


def get_template_env() -> Environment:
    """Get the Jinja2 template environment."""
    template_dir = Path(__file__).parent.parent / "templates"
    return Environment(loader=FileSystemLoader(template_dir))


def generate_travel_document(
    traveler_name: str,
    destination: str,
    country: str,
    check_in_date: str,
    check_out_date: str,
    hotel_name: str,
    hotel_address: str,
    hotel_rating: int,
    room_type: str,
    board_type: str,
    flight_outbound: str,
    flight_return: str,
    total_price: str,
    events: list[dict],
    attractions: list[dict],
    restaurants: list[dict],
    activities: list[dict],
    practical_tips: list[dict],
    weather_info: str,
    booking_reference: Optional[str] = None,
) -> str:
    """
    Generate an HTML travel document with all travel information.

    Args:
        traveler_name: Name of the traveler(s)
        destination: Destination city/region
        country: Destination country
        check_in_date: Hotel check-in date (YYYY-MM-DD format)
        check_out_date: Hotel check-out date (YYYY-MM-DD format)
        hotel_name: Name of the hotel
        hotel_address: Full address of the hotel
        hotel_rating: Hotel star rating (1-5)
        room_type: Type of room booked
        board_type: Meal plan (e.g., "All Inclusive", "Half Board", "Breakfast")
        flight_outbound: Outbound flight details
        flight_return: Return flight details
        total_price: Total price of the trip
        events: List of local events during the stay
        attractions: List of recommended attractions
        restaurants: List of recommended restaurants
        activities: List of recommended activities
        practical_tips: List of practical tips for the destination
        weather_info: Expected weather information
        booking_reference: Optional booking reference number

    Returns:
        HTML string of the generated travel document
    """
    env = get_template_env()
    template = env.get_template("travel_document.html")

    # Calculate duration
    try:
        check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
        duration_nights = (check_out - check_in).days
        formatted_check_in = check_in.strftime("%A, %B %d, %Y")
        formatted_check_out = check_out.strftime("%A, %B %d, %Y")
    except ValueError:
        duration_nights = "N/A"
        formatted_check_in = check_in_date
        formatted_check_out = check_out_date

    html_content = template.render(
        traveler_name=traveler_name,
        destination=destination,
        country=country,
        check_in_date=formatted_check_in,
        check_out_date=formatted_check_out,
        duration_nights=duration_nights,
        hotel_name=hotel_name,
        hotel_address=hotel_address,
        hotel_rating=hotel_rating,
        hotel_stars="★" * hotel_rating + "☆" * (5 - hotel_rating),
        room_type=room_type,
        board_type=board_type,
        flight_outbound=flight_outbound,
        flight_return=flight_return,
        total_price=total_price,
        events=events,
        attractions=attractions,
        restaurants=restaurants,
        activities=activities,
        practical_tips=practical_tips,
        weather_info=weather_info,
        booking_reference=booking_reference or "TRV-" + datetime.now().strftime("%Y%m%d%H%M"),
        generated_date=datetime.now().strftime("%B %d, %Y at %H:%M"),
    )

    return html_content


def save_document_to_file(
    html_content: str,
    output_filename: str,
    output_format: str = "html",
) -> str:
    """
    Save the generated travel document to a file.

    Args:
        html_content: The HTML content of the travel document
        output_filename: Base filename (without extension)
        output_format: Output format - "html" or "pdf"

    Returns:
        Path to the saved file
    """
    # Create output directory if it doesn't exist
    output_dir = Path("./travel_documents")
    output_dir.mkdir(exist_ok=True)

    if output_format == "html":
        output_path = output_dir / f"{output_filename}.html"
        output_path.write_text(html_content, encoding="utf-8")
        return str(output_path.absolute())

    elif output_format == "pdf":
        try:
            from weasyprint import HTML

            output_path = output_dir / f"{output_filename}.pdf"
            HTML(string=html_content).write_pdf(output_path)
            return str(output_path.absolute())
        except ImportError:
            # Fallback to HTML if WeasyPrint is not available
            output_path = output_dir / f"{output_filename}.html"
            output_path.write_text(html_content, encoding="utf-8")
            return f"{output_path.absolute()} (PDF generation requires WeasyPrint)"

    else:
        raise ValueError(f"Unsupported output format: {output_format}")
