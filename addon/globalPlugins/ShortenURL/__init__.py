# -*- coding: utf-8 -*-
# Copyright (C) 2020 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import gui
import globalPluginHandler
from scriptHandler import script
import addonHandler
import globalVars
import ui
import api
import sys, os
sys.path.append(os.path.dirname(__file__))
import validators
import acortadores

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		# Call of the constructor of the parent class.
		super(GlobalPlugin, self).__init__()
		self._MainWindows = None

		if globalVars.appArgs.secure:
			return

		# Creation of our menu.
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		# Translators: Name of the item in the tools menu
		self.menuItem = self.toolsMenu.Append(wx.ID_ANY, _("&AcortadorURL"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.dlgPrincipal, self.menuItem)

	def terminate(self):
		try:
			if not self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass

	def dlgPrincipal(self, event):
		if not self._MainWindows:
			self._MainWindows = Dialogo(gui.mainFrame)
		if not self._MainWindows.IsShown():
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

	# Translators: Description for the input gesture panel
	@script(gesture=None, description= _("Activar la ventana de AcortadorURL"),
		# Translators: Category name in panel entry gestures
		category= _("AcortadorURL"))
	def script_ShortenURL(self, gesture):
		wx.CallAfter(self.dlgPrincipal, None)

class Dialogo(wx.Dialog):
# Function taken from the add-on emoticons to center the window
	def _calculatePosition(self, width, height):
		w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
		h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
		# Centre of the screen
		x = w / 2
		y = h / 2
		# Minus application offset
		x -= (width / 2)
		y -= (height / 2)
		return (x, y)

	def validaUrl(self, url):
		if not validators.url(url):
			return False
		else:
			return True

	def __init__(self, parent):
		WIDTH = 500
		HEIGHT = 350
		pos = self._calculatePosition(WIDTH, HEIGHT)

		# Translators: Window title
		super(Dialogo, self).__init__(parent, -1, title=_("AcortadorURL"), pos = pos, size = (WIDTH, HEIGHT))

		panel_dialogo = wx.Panel(self)

		self.indice = 0

		# Translators: Label for the service combo box
		label1 = wx.StaticText(panel_dialogo, wx.ID_ANY, label=_("&Servicios acortadores disponibles:"))
		acortadores = ["Acortame", "Clckru", "Isgd", "Tinyurl"] # "Relink"
		self.choice = wx.Choice(panel_dialogo, wx.ID_ANY, choices = acortadores) 
		self.choice.SetSelection(0)
		self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)

		# Translators: Label for the URL shortening field
		label2 = wx.StaticText(panel_dialogo, wx.ID_ANY, label=_("&url para acortar:"))
		self.textoOrigen = wx.TextCtrl(panel_dialogo, wx.ID_ANY,style = wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)
		self.Bind(wx.EVT_TEXT_ENTER, self.Txt_Ent, self.textoOrigen)

		# Translators: shorten url button name
		self.AcortaBTN = wx.Button(panel_dialogo, wx.ID_ANY, _("&Acortar URL"))
		self.Bind(wx.EVT_BUTTON, self.Txt_Ent, self.AcortaBTN)

		# Translators: Label for the result field with shortened url
		label3 = wx.StaticText(panel_dialogo, wx.ID_ANY, label=_("&Dirección URL acortada:"))
		self.textoDestino = wx.TextCtrl(panel_dialogo, wx.ID_ANY, style= wx.TE_READONLY |wx.HSCROLL | wx.TE_MULTILINE)

		# Translators: Copy to clipboard button name
		self.CopyClipboardBTN = wx.Button(panel_dialogo, wx.ID_ANY, _("&Copiar al portapapeles"))
		self.Bind(wx.EVT_BUTTON, self.onCopyClipboard, self.CopyClipboardBTN)

		# Translators: Exit button name
		self.ExitBTN = wx.Button(panel_dialogo, wx.ID_CANCEL, _("Salir Alt+F4"))
		self.Bind(wx.EVT_BUTTON, self.onExit, id=wx.ID_CANCEL)
		self.Bind(wx.EVT_CLOSE, self.onExit)

		self.Bind(wx.EVT_SET_FOCUS, self.onFocus)

		sizerV = wx.BoxSizer(wx.VERTICAL)
		sizerH = wx.BoxSizer(wx.HORIZONTAL)

		sizerV.Add(label1, 0, wx.EXPAND | wx.ALL)
		sizerV.Add(self.choice, 0, wx.EXPAND | wx.ALL)

		sizerV.Add(label2, 0, wx.EXPAND | wx.ALL)
		sizerV.Add(self.textoOrigen, 0, wx.EXPAND | wx.ALL)
		sizerV.Add(self.AcortaBTN, 0, wx.EXPAND)

		sizerV.Add(label3, 0, wx.EXPAND | wx.ALL)
		sizerV.Add(self.textoDestino, 0, wx.EXPAND | wx.ALL)

		sizerH.Add(self.CopyClipboardBTN, 2, wx.CENTER)
		sizerH.Add(self.ExitBTN, 2, wx.CENTER)

		sizerV.Add(sizerH, 0, wx.CENTER)

		panel_dialogo.SetSizer(sizerV)

	def onFocus(self, event):
		self.textoOrigen.SetFocus()

	def OnChoice(self, event):
		self.indice = event.GetSelection()
		self.textoOrigen.Clear()
		self.textoDestino.Clear()

	def Txt_Ent(self,event):
		self.textoDestino.Clear()
		if self.indice == 0:
			acortador = acortadores.AcortameShortener()
		elif self.indice == 1:
			acortador = acortadores.ClckruShortener()
		elif self.indice == 2:
			acortador = acortadores.IsgdShortener()
#		elif self.indice == 3:
#			acortador = acortadores.RelinkShortener()
		elif self.indice == 3:
			acortador = acortadores.TinyurlShortener()

		if self.textoOrigen.GetValue() == "":
			# Translators: Tells the user that he cannot leave the field blank
			msg = \
_("""No puedes dejar el campo de la url en blanco para acortar.
Asegúrate de introducir una URL correcta.""")
			gui.messageBox(msg,
				# Translators: Message window title: Error
				_("Error"), wx.ICON_ERROR)
			self.textoOrigen.SetFocus()
		else:
			if not self.validaUrl(self.textoOrigen.GetValue()):
				# Translators: Error message, the url is not valid
				msg = \
_("""La URL que a introducido no es correcta.
Asegúrese de introducir una URL valida.""")
				gui.messageBox(msg,
					# Translators: Message window title: Error
					_("Error"), wx.ICON_ERROR)
				self.textoOrigen.Clear()
				self.textoOrigen.SetFocus()
			else:
				try:
					urlReducida = acortador._shorten(self.textoOrigen.GetValue())
					self.textoDestino.SetValue(urlReducida)
					self.textoDestino.SetFocus()
				except:
					# Translators: Error message, service failed
					msg = \
_("""No se pudo generar la URL acortada.
La conexión con el servicio fallo.
Inténtelo de nuevo y si el problema persiste elija otro servicio acortador.""")
					gui.messageBox(msg,
						# Translators: Message window title: Error
						_("Error"), wx.ICON_ERROR)
					self.textoOrigen.SetFocus()

	def onCopyClipboard (self, event):
		if self.textoDestino.GetValue() == "":
			# Translators: Error message, nothing to copy to clipboard
			msg = \
_("""No hay ninguna URL acortada.
Tiene que generar una antes para copiarla al portapapeles.""")
			gui.messageBox(msg,
				# Translators: Message window title: Error
				_("Error"), wx.ICON_ERROR)
			self.textoOrigen.SetFocus()
		else:
			api.copyToClip(self.textoDestino.GetValue())
			ui.message(_("Se a copiado la URL al portapapeles. Ya puede compartirla."))

	def onExit(self, event):
		self.Destroy()
		gui.mainFrame.postPopup()


