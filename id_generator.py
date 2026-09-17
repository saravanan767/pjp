from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

st.set_page_config(
    page_title="PJK Membership ID Generator", page_icon="🦋", layout="centered"
)

st.title("🦋 Pattamoochi Jananayaga Katchi (PJK)")
st.subheader("Official Digital Membership ID Card Generator")

# User Input Form
with st.form("id_card_form"):
    member_name = st.text_input("Member Name", "A. KUMARESAN")
    member_id = st.text_input("Member ID", "PJK/TN/2024/00001")
    district = st.text_input("District", "TRICHY")
    designation = st.text_input("Designation", "FOUNDER / PRESIDENT")
    uploaded_file = st.file_uploader(
        "Upload Member Photo (Passport Size)", type=["jpg", "jpeg", "png"]
    )

    submitted = st.form_submit_button("Generate ID Card")

if submitted:
  # Base Dimensions matching standard vertical ID cards
  card_width, card_height = 800, 1150
  card = Image.new("RGB", (card_width, card_height), "#ffffff")
  draw = ImageDraw.Draw(card)

  # Colors
  maroon = (107, 0, 0)
  gold = (212, 175, 55)
  dark_text = (34, 34, 34)

  # 1. Top Header Banner
  draw.rectangle([(0, 0), (card_width, 220)], fill=maroon)
  draw.rectangle([(0, 215), (card_width, 225)], fill=gold)

  # Load standard fonts ( fallbacks to default if custom ttf paths aren't local )
  try:
    font_title = ImageFont.truetype("arial.ttf", 36)
    font_subtitle = ImageFont.truetype("arial.ttf", 22)
    font_body = ImageFont.truetype("arial.ttf", 26)
  except IOError:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_body = ImageFont.load_default()

  # Header Text
  draw.text(
      (220, 50),
      "PJK MEMBERSHIP CARD",
      fill=(255, 255, 255),
      font=font_title,
  )
  draw.text(
      (220, 110),
      "PATTAMPOOCHI JANANAYAGA KATCHI",
      fill=gold,
      font=font_subtitle,
  )

  # 2. Member Photo Placement Box
  photo_box_box = [(60, 320), (420, 780)]
  draw.rounded_rectangle(
      photo_box_box, radius=15, outline=gold, width=4, fill=(245, 245, 245)
  )

  if uploaded_file is not None:
    user_img = Image.open(uploaded_file)
    user_img = user_img.resize((348, 448))
    card.paste(user_img, (66, 326))

  # 3. Member Details Text Block
  start_x = 460
  start_y = 330
  line_spacing = 65

  details = [
      ("Member Name:", member_name),
      ("Member ID:", member_id),
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
        (start_x, start_y + 25), value, fill=dark_text, font=font_body
    )
    start_y += line_spacing

  # 4. Bottom Footer Banner
  draw.rectangle(
      [(0, card_height - 150), (card_width, card_height)], fill=maroon
  )
  draw.rectangle(
      [(0, card_height - 155), (card_width, card_height - 150)], fill=gold
  )

  footer_text_1 = "Pannappatty, Manapparai, Trichy • Phone: 8870942555"
  footer_text_2 = (
      "Issued by: PATTAMPOOCHI JANANAYAGA KATCHI (PJK), TAMIL NADU, INDIA"
  )

  draw.text((40, card_height - 120), footer_text_1, fill=(255, 255, 255), font=font_subtitle)
  draw.text((40, card_height - 75), footer_text_2, fill=gold, font=font_subtitle)

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
