from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import datetime
import locale
from tkinter import *
import webbrowser
import os
locale.setlocale(locale.LC_ALL, '')
logo = "Logo-TripleConsult.jpg"
gui = Tk()
gui.title("Rechnung erstellen")
gui.geometry("580x220")
edit_text_names = ["Rechnungsnummer", "Firmenname", "Zeichen", "Stundenpreis", "Stunden", "Straße mit Hausnummer", "PLZ", "Ort", "Ab", "Bis", "Beschreibung"]
fname = ""


def checkforint(string):  # wenn max nicht angegeben wird, checkt die Funktion nur nach int
    return string.isdigit()



def checklen(string):
    if string.isdigit():
        #if max != 0:
        return len(string) <= 5
        #else:

    else:
        return False


def checkformonth(index):
    months = ["januar", "februar", "märz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]
    if textboxes3[index].get().lower() in months:
        return True
    else:
        textboxes3[index].delete(0, len(textboxes3[index].get()))
        return False


def checkdate():
    global block_save
    list = textboxes1[0].get().split(".")
    try:
        datetime.date(int(list[2]),int(list[1]), int(list[0]))
        textboxes1[0].config(foreground="black")
        block_save = False
        return True
    except:
        textboxes1[0].config(foreground="red")
        block_save = True
        return False


def rechnung_oeffnen(fname):
    try:
        if os.path.exists(fname):
            webbrowser.open_new(r"{}".format(os.path.abspath(fname)))
    except:
        pass


def daten_holen():
    daten = {}
    datumsdaten = textboxes1[0].get().split(".")
    if len(datumsdaten) == 3:
        daten["Datum"] = datetime.date(int(datumsdaten[2]), int(datumsdaten[1]), int(datumsdaten[0]))
    else:
        daten["Datum"] = ""
    daten.update({key: textbox.get() for key, textbox in zip(edit_text_names, textboxes1[1:] + textboxes2 + textboxes3 + [beschreibung])})
    return daten


def geld_berechnen(stundenpreis, stunden):
    geld = stundenpreis.split(",")
    stundenpreis_float = float(geld[0] + "." + geld[1])
    gesamt_preis_float = stundenpreis_float * int(stunden)
    gesamt_preis_list = str(gesamt_preis_float).split(".")
    gesamt_preis_list[1] += "00"
    gesamt_preis_list[1] = gesamt_preis_list[1][:2]
    gesamt_preis_string = "{:n}".format(int(gesamt_preis_list[0])) + "," + gesamt_preis_list[1]
    umsatzsteuer = gesamt_preis_float/100*16
    umsatzsteuer_string = punkt_zu_komma(umsatzsteuer)
    preis_mit_steuer = umsatzsteuer + gesamt_preis_float
    preis_mit_steuer_string = punkt_zu_komma(preis_mit_steuer)
    return [gesamt_preis_string, umsatzsteuer_string, preis_mit_steuer_string]


def draw_label(text, column, row):
    label = Label(gui, text=text)
    label.grid(row=row, column=column,sticky="E")


def draw_labels_textboxes(texts, column, row_start, textbox_width):
    text_box_list = []
    for text in texts:
        label = Label(gui, text=text)
        text_box_list.append(Entry(gui, width=textbox_width))
        label.grid(row=row_start, column=column, sticky="E")
        text_box_list[-1].grid(row=row_start, column=column + 1)
        row_start += 1
    return text_box_list


def punkt_zu_komma(zahl):
    zahl_list = str(zahl).split(".")
    zahl_list[1] += "0"
    zahl_list[1] = zahl_list[1][:2]
    zahl_string = f"{float(zahl):,.2f}"
    res = []
    my_replace = {',': '.', '.': ','}
    for c in zahl_string:
        if c in my_replace.keys():
            res.append(my_replace[c])
        else:
            res.append(c)
    return "".join(res)


def autolines(text, max_width, font, fontsize):  # man gibt text und max breite ein und kriegt die passenden zeilen in einer liste wieder zurück
    words_list = text.split(" ")
    teststring = words_list.pop(0)
    textlines = []
    last_time = True
    while len(words_list) > 0:
        string_width = pdf.stringWidth(teststring, font, fontsize)/mm
        if string_width > max_width:  # länger als max
            liste = teststring.split(" ")
            words_list.insert(0, liste.pop())
            last_time = False
            teststring = " ".join(liste)
        else:  # kürzer als max
            if not last_time:
                textlines.append(teststring)
                teststring = words_list.pop(0)
                last_time = True
            else:
                teststring += " " + words_list.pop(0)
    else:
        textlines.append(teststring)
    return textlines


def datenausgefuellt():
    global daten
    daten = daten_holen()
    for k, v in daten.items():
        if v == "":
            if k == "Bis":
                continue
            break
    else:
        if not block_save:
            pdf_zeichnen_saven(daten)


def pdf_zeichnen_saven(daten):
    global pdf, fname
    fname = f"Rechnung_{daten['Firmenname']}_{daten['Rechnungsnummer']}.pdf"
    pdf = canvas.Canvas(fname)
    geld_beträge = geld_berechnen(daten["Stundenpreis"],daten["Stunden"])
    pdf.setFontSize(6)
    pdf.setFillColorRGB(150/256, 150/256, 150/256)
    pdf.drawString(22*mm, 249*mm, "Muster GmbH, Oberweg 19, 45687 Hamburg")
    pdf.setFontSize(10)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(22*mm, 239*mm, "Firma")
    pdf.drawString(22*mm, 235*mm, daten["Firmenname"])
    pdf.drawString(22*mm, 231*mm, daten["Straße mit Hausnummer"])
    pdf.drawString(22*mm, 227*mm, daten["PLZ"] + " " + daten["Ort"])
    pdf.setFontSize(8)
    pdf.setFillColorRGB(50/256, 50/256, 50/256)
    pdf.drawString(128*mm, 234*mm, "Zeichen:")
    pdf.drawString(128*mm, 230*mm, "Mobil:")
    pdf.drawString(128*mm, 226*mm, "Telefax:")
    pdf.drawString(128*mm, 222*mm, "E-Mail:")
    pdf.drawString(142*mm, 234*mm, daten["Zeichen"])
    pdf.drawString(142*mm, 230*mm, '+49 12345 678910')
    pdf.drawString(142*mm, 226*mm, '+49 12345 678910')
    pdf.drawString(142*mm, 222*mm, 'info@muster.de')
    pdf.drawInlineImage(logo, 126*mm, 249*mm, 55*mm, 31*mm)  # Logo hinzufügen
    # Haupttext mit Überschrift
    pdf.setFillColorRGB(50/256, 50/256, 50/256)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(22*mm, 189*mm, "Rechnung " + daten["Rechnungsnummer"])
    pdf.setFont("Helvetica", 12)
    pdf.drawString(22*mm, 176*mm, "Sehr geehrte Damen und Herren,")
    if not daten["Bis"] == "":
        ersteZeile = f"für die Beratung und Softwareentwicklung in den Monaten {daten['Ab'].title()} bis {daten['Bis'].title()}"
        zweiteZeile = "stellen wir ihnen gemäß Vereinbarung folgende Positionen in Rechnung:"
    else:
        ersteZeile = f"für die Beratung und Softwareentwicklung im Monat {daten['Ab'].title()} stellen wir ihnen"
        zweiteZeile = "gemäß Vereinbarung folgende Positionen in Rechnung:"
    pdf.drawString(22*mm, 170*mm, ersteZeile)
    pdf.drawString(22*mm, 164*mm, zweiteZeile)
    pdf.setFontSize(11)
    pdf.drawString(164*mm, 202*mm, daten["Datum"].strftime("%d.%m.%Y"))
    pdf.line(22*mm, 156*mm, 180*mm, 156*mm)
    pdf.line(22*mm, 150*mm, 180*mm, 150*mm)
     # Unterer Teil
    pdf.setFontSize(8)
    pdf.setFillColorRGB(0.4, 0.4, 0.4)
    pdf.line(22*mm, 30*mm, 180*mm, 30*mm)

    # Rechnungsteil
    pdf.setFillColorRGB(50/256, 50/256, 50/256)
    pdf.setFontSize(10)
    pdf.drawString(23*mm, 152*mm, "Pos.")
    pdf.drawString(36*mm, 152*mm, "Beschreibung")
    pdf.drawString(127*mm, 152*mm, "h")  # Ende des Strings: 129
    pdf.drawString(136*mm, 152*mm, "Einzel (€)")  # Width = 14.89, Ende des Strings:151
    pdf.drawString(161*mm, 152*mm, "Gesamt (€)")  # Width = 17.64, Ende des Strings:
    pdf.drawString((129-(pdf.stringWidth(daten["Stunden"], "Helvetica", 10)/mm))*mm, 146*mm, daten["Stunden"])
    pdf.drawString((151-(pdf.stringWidth(daten["Stundenpreis"], "Helvetica", 10)/mm))*mm, 146*mm, daten["Stundenpreis"])
    pdf.drawString((179-(pdf.stringWidth(geld_beträge[0], "Helvetica", 10)/mm))*mm, 146*mm, geld_beträge[0])
    pdf.drawString(23*mm, 146*mm, "1")
    text = pdf.beginText(36*mm, 146*mm)
    lines = autolines(daten["Beschreibung"], 70, "Helvetica", 10)
    text.setFont("Helvetica", 10)
    for line in lines:
        text.textLine(line)
    pdf.drawText(text)
    summe_netto_hoehe = 142 - 4.8 * len(lines)
    pdf.drawString(129.5*mm, summe_netto_hoehe*mm, "Summe Netto")
    pdf.line(119*mm, (summe_netto_hoehe - 2)*mm, 180*mm, (summe_netto_hoehe - 2)*mm)
    pdf.drawString(121*mm, (summe_netto_hoehe - 6)*mm, "Umsatzsteuer 16%")
    pdf.line(119*mm, (summe_netto_hoehe - 8)*mm, 180*mm, (summe_netto_hoehe - 8)*mm)
    pdf.drawString(123*mm, (summe_netto_hoehe - 12)*mm, "Rechnungsbetrag")
    pdf.line(119*mm, (summe_netto_hoehe - 14)*mm, 180*mm, (summe_netto_hoehe - 14)*mm)
    pdf.line(119*mm, (summe_netto_hoehe - 14.7)*mm, 180*mm, (summe_netto_hoehe - 14.7)*mm)
    pdf.drawString((179-(pdf.stringWidth("€ " + geld_beträge[0], "Helvetica", 10)/mm))*mm, summe_netto_hoehe*mm, "€ " + geld_beträge[0])
    pdf.drawString((179-(pdf.stringWidth("€ " + geld_beträge[1], "Helvetica", 10)/mm))*mm, (summe_netto_hoehe - 6)*mm, "€ " + geld_beträge[1])
    pdf.drawString((179-(pdf.stringWidth("€ " + geld_beträge[2], "Helvetica", 10)/mm))*mm, (summe_netto_hoehe - 12)*mm, "€ " + geld_beträge[2])
    pdf.setFontSize(12)
    text_mit_datum = "Rechnungsbetrag bis zum {:%d.%m.%Y} ohne Abzug auf unten genanntes Konto."
    add30days = datetime.timedelta(30)
    pdf.drawString(22*mm, (summe_netto_hoehe - 26)*mm, "Wir bedanken uns für das entgegengebrachte Vertrauen. Bitte überweisen Sie den")
    pdf.drawString(22*mm, (summe_netto_hoehe - 32)*mm, text_mit_datum.format(daten["Datum"] + add30days))
    pdf.drawString(22*mm, ((summe_netto_hoehe - 62) / 2 + 35)*mm, "Mit freundlichen Grüßen")
    pdf.drawString(22*mm, ((summe_netto_hoehe - 62) / 2 + 23)*mm, "Benjamin Jacob")
    pdf.setTitle("Rechnung " + daten["Rechnungsnummer"])
    pdf.save()
datecheck = gui.register(checkdate)
ab = gui.register(lambda: checkformonth(0))
bis = gui.register(lambda: checkformonth(1))
intcheck = gui.register(checkforint)
lencheck = gui.register(checklen)

draw_label("Daten eingeben:",0,0)
textboxes1 = draw_labels_textboxes(["Rechnungsdatum","Rechnungsnummer","Firmenname","Zeichen","Stundenpreis","Gesamtzahl Stunden"],0,1,25)
textboxes2 = draw_labels_textboxes(["Straße HausNr.", "Postleitzahl","Ort"],3,1,25)
textboxes3 = draw_labels_textboxes(["Ab","Bis (kein Pflichtfeld)"],3,5,25)
beschreibung = Entry(gui,width=70)
textboxes1[4].insert(0,"25,00")

draw_label("Addresse", 3,0)

btn_drawsave = Button(gui, text="Speichern", command=datenausgefuellt)
btn_open = Button(gui,text="Öffnen",command=lambda: rechnung_oeffnen(fname))
btn_drawsave.grid(row=10,column=0)
btn_open.grid(row=10,column=1, sticky="W")
draw_label("Beschreibung", 0,8)
draw_label("der Dienstleistung", 0,9)
leistungszeitraum = Label(gui, text='Leistungszeitraum in Monaten ("Juni", nicht 6)')
leistungszeitraum.grid(row=4,column=3, columnspan=2)
beschreibung.grid(row=9,column=1,columnspan=4)

textboxes1[0].config(validate="focusout", validatecommand= datecheck)
textboxes3[0].config(validate="focusout", validatecommand=ab)
textboxes3[1].config(validate="focusout", validatecommand=bis)
textboxes1[5].config(validate="key", validatecommand=(intcheck, "%S"))
textboxes2[1].config(validate="key", validatecommand=(lencheck, "%P"))

gui.mainloop()
