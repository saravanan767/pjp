from datetime import datetime
from pathlib import Path
import secrets
from PIL import Image, ImageDraw, ImageFont, ImageOps
import streamlit as st

st.set_page_config(
    page_title="PJP Membership ID Generator", page_icon="🦋", layout="centered"
)

st.title("🦋 Pattamoochi Jananayaga Katchi (PJK)")
st.subheader("Official Digital Membership ID Card Generator")

if "auto_member_id" not in st.session_state:
  random_sequence = secrets.randbelow(99999) + 1
  st.session_state.auto_member_id = f"PJK/TN/2026/{random_sequence:05d}"
auto_member_id = st.session_state.auto_member_id

# User Input Form
with st.form("id_card_form"):
    member_name = st.text_input("Member Name", "")
    
    st.text_input("Member ID (Auto-Generated)", value=auto_member_id, disabled=True)
    
    district = st.text_input("District", "")
    
    # Designation forced to default to 'MEMBER'
    designation = st.text_input("Designation", "MEMBER")
    
    uploaded_file = st.file_uploader(
        "Upload Member Photo (Passport Size)", type=["jpg", "jpeg", "png"]
    )

    submitted = st.form_submit_button("Generate ID Card")

if submitted:
  # Standard portrait ID card proportions.
  card_width, card_height = 640, 1024
  card = Image.new("RGB", (card_width, card_height), "#ffffff")
  draw = ImageDraw.Draw(card)

  # Colors
  maroon = (107, 0, 0)
  gold = (212, 175, 55)
  dark_text = (34, 34, 34)

  # 1. Top Header Banner
  draw.rectangle([(0, 0), (card_width, 225)], fill=maroon)
  draw.rectangle([(0, 220), (card_width, 230)], fill=gold)

  # Load standard fonts ( fallbacks to default if custom ttf paths aren't local )
  try:
    font_title = ImageFont.truetype("arial.ttf", 34)
    font_subtitle = ImageFont.truetype("arial.ttf", 24)
    font_body = ImageFont.truetype("arial.ttf", 28)
    font_footer = ImageFont.truetype("arial.ttf", 14)
  except IOError:
    try:
      font_title = ImageFont.truetype("DejaVuSans.ttf", 34)
      font_subtitle = ImageFont.truetype("DejaVuSans.ttf", 24)
      font_body = ImageFont.truetype("DejaVuSans.ttf", 28)
      font_footer = ImageFont.truetype("DejaVuSans.ttf", 14)
    except IOError:
      font_title = ImageFont.load_default()
      font_subtitle = ImageFont.load_default()
      font_body = ImageFont.load_default()
      font_footer = ImageFont.load_default()

  # Header logo and centered card title
  logo = Image.open(Path(__file__).with_name("logo.png")).convert("RGB")
  logo = ImageOps.contain(logo, (100, 100))
  card.paste(logo, (28 + (100 - logo.width) // 2, 48 + (100 - logo.height) // 2))

  header_center_x = (145 + card_width) // 2
  draw.text(
    (header_center_x, 30),
    "PATTAMPOOCHI",
    fill=(255, 255, 255),
    font=font_title,
    anchor="mt",
  )
  draw.text(
    (header_center_x, 75),
    "JANANAYAGA KATCHI",
    fill=gold,
    font=font_title,
    anchor="mt",
  )
  draw.text(
    (header_center_x, 155),
    "MEMBERSHIP ID CARD",
    fill=(255, 255, 255),
    font=font_subtitle,
    anchor="mt",
  )

  # 2. Member Photo Placement Box
  photo_box_box = [(40, 280), (260, 580)]
  draw.rounded_rectangle(
    photo_box_box, radius=15, outline=gold, width=4, fill=(245, 245, 245)
  )

  if uploaded_file is not None:
    user_img = ImageOps.fit(
      Image.open(uploaded_file).convert("RGB"), (208, 292)
    )
    card.paste(user_img, (46, 284))

  # 3. Member Details Text Block (Using the auto-generated ID & default designation)
  start_x = 295
  start_y = 280
  line_spacing = 88

  details = [
    ("Member Name:", member_name),
    ("Member ID:", auto_member_id),
    ("District:", district),
    (
      "Date of Joining:",
      datetime.now().strftime("%d-%b-%Y").upper(),
    ),
    ("Designation:", designation),
  ]

  for label, value in details:
    draw.text((start_x, start_y), label, fill=maroon, font=font_subtitle)
    draw.text(
      (start_x, start_y + 32), value, fill=dark_text, font=font_body
    )
    start_y += line_spacing

  # 4. Bottom Footer Banner
  draw.rectangle(
    [(0, card_height - 120), (card_width, card_height)], fill=maroon
  )
  draw.rectangle(
    [(0, card_height - 125), (card_width, card_height - 120)], fill=gold
  )

  footer_text_1 = "Pannappatty, Manapparai, Trichy • Phone: 8870942555"
  footer_text_2 = (
    "Issued by: PATTAMPOOCHI JANANAYAGA KATCHI (PJK), TAMIL NADU, INDIA"
  )

  draw.text(
    (card_width // 2, card_height - 95),
    footer_text_1,
    fill=(255, 255, 255),
    font=font_footer,
    anchor="mm",
  )
  draw.text(
    (card_width // 2, card_height - 55),
    footer_text_2,
    fill=gold,
    font=font_footer,
    anchor="mm",
  )

  # Display Generated Card in Streamlit
  st.success("ID Card generated successfully!")
  st.image(card, caption="Generated PJK Membership Card", use_container_width=True)

  # Save option
  card.save("pjk_membership_card.png")
  with open("pjk_membership_card.png", "rb") as file:
    st.download_button(
      label="Download ID Card",
      data=file,
      file_name="pjk_membership_card.png",
      mime="image/png",
    )
