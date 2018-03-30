# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#


# GUIWORLD.py - scripts to control some windows from GUIWORLD winpack
#    except of Actions, Portrait, Options and Dialog windows

###################################################

import GemRB
import GUICommon
import GUICommonWindows
import CommonWindow
from GUIDefines import *
import MessageWindow

FormationWindow = None
ReformPartyWindow = None

def DialogStarted ():
	global ContinueWindow

	GUICommonWindows.CloseTopWindow()
	CommonWindow.CloseContainerWindow()

	# opening control size to maximum, enabling dialog window
	CommonWindow.SetGameGUIHidden(False)
	GemRB.GameSetScreenFlags(GS_DIALOG, OP_OR)

def DialogEnded ():
	pass

def CloseContinueWindow ():
	# don't close the actual window now to avoid flickering: we might still want it open
	GemRB.SetVar ("DialogChoose", GemRB.GetVar ("DialogOption"))

def NextDialogState ():
	if not MessageWindow.MWindow:
		return

	Button = MessageWindow.MWindow.GetControl (0)
	Button.SetText(28082)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, lambda: MessageWindow.MWindow.Close())

def OpenEndMessageWindow ():
	Button = MessageWindow.MWindow.GetControl (0)
	Button.SetText (34602)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, CloseContinueWindow)
	Button.MakeDefault()
	Button.Focus()

def OpenContinueMessageWindow ():
	#continue
	Button = MessageWindow.MWindow.GetControl (0)
	Button.SetText (34603)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, CloseContinueWindow)
	Button.MakeDefault()
	Button.Focus()

def OpenReformPartyWindow ():
	global ReformPartyWindow

	if GUICommon.CloseOtherWindow(OpenReformPartyWindow):
		if ReformPartyWindow:
			ReformPartyWindow.Unload ()
		ReformPartyWindow = None

		GemRB.SetVar ("OtherWindow", -1)
		GUICommonWindows.EnableAnimatedWindows ()
		return

	ReformPartyWindow = Window = GemRB.LoadWindow (24, GUICommon.GetWindowPack())
	GemRB.SetVar ("OtherWindow", Window.ID)
	GUICommonWindows.DisableAnimatedWindows ()

	# Remove
	Button = Window.GetControl (15)
	Button.SetText (42514)
	Button.SetState (IE_GUI_BUTTON_DISABLED)
	# TODO: implement removal

	# Done
	Button = Window.GetControl (8)
	Button.SetText (1403)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, OpenReformPartyWindow)


last_formation = None

def OpenFormationWindow ():
	global FormationWindow

	if GUICommon.CloseOtherWindow(OpenFormationWindow):
		if FormationWindow:
			FormationWindow.Unload ()
		FormationWindow = None

		GemRB.GameSetFormation (last_formation, 0)
		GUICommonWindows.EnableAnimatedWindows ()
		GemRB.SetVar ("OtherWindow", -1)
		return

	FormationWindow = Window = GemRB.LoadWindow (27, GUICommon.GetWindowPack())
	GemRB.SetVar ("OtherWindow", Window.ID)
	GUICommonWindows.DisableAnimatedWindows ()

	# Done
	Button = Window.GetControl (13)
	Button.SetText (1403)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, OpenFormationWindow)

	tooltips = (
		44957,  # Follow
		44958,  # T
		44959,  # Gather
		44960,  # 4 and 2
		44961,  # 3 by 2
		44962,  # Protect
		48152,  # 2 by 3
		44964,  # Rank
		44965,  # V
		44966,  # Wedge
		44967,  # S
		44968,  # Line
		44969,  # None
	)

	for i in range (13):
		Button = Window.GetControl (i)
		Button.SetVarAssoc ("SelectedFormation", i)
		Button.SetTooltip (tooltips[i])
		Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, SelectFormation)

	GemRB.SetVar ("SelectedFormation", GemRB.GameGetFormation (0))
	SelectFormation ()

def SelectFormation ():
	global last_formation
	Window = FormationWindow
	
	formation = GemRB.GetVar ("SelectedFormation")
	print "FORMATION:", formation
	if last_formation != None and last_formation != formation:
		Button = Window.GetControl (last_formation)
		Button.SetState (IE_GUI_BUTTON_UNPRESSED)

	Button = Window.GetControl (formation)
	Button.SetState (IE_GUI_BUTTON_SELECTED)

	last_formation = formation
