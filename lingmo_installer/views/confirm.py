# dialog.py
#
# Copyright 2024 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from gettext import gettext as _

from gi.repository import Adw, GObject, Gtk


@Gtk.Template(resource_path="/org/lingmoos/Installer/gtk/widget-choice.ui")
class LingmoChoiceEntry(Adw.ActionRow):
    __gtype_name__ = "LingmoChoiceEntry"

    img_choice = Gtk.Template.Child()

    def __init__(self, title, subtitle, icon_name, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.img_choice.set_from_icon_name(icon_name)


@Gtk.Template(resource_path="/org/lingmoos/Installer/gtk/widget-choice-expander.ui")
class LingmoChoiceExpanderEntry(Adw.ExpanderRow):
    __gtype_name__ = "LingmoChoiceExpanderEntry"

    img_choice = Gtk.Template.Child()

    def __init__(self, title, subtitle, icon_name, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.img_choice.set_from_icon_name(icon_name)


@Gtk.Template(resource_path="/org/lingmoos/Installer/gtk/confirm.ui")
class LingmoConfirm(Adw.Bin):
    __gtype_name__ = "LingmoConfirm"
    __gsignals__ = {
        "installation-confirmed": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    group_changes = Gtk.Template.Child()
    btn_confirm = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

    def update(self, finals):
        try:
            for widget in self.active_widgets:
                self.group_changes.remove(widget)
        except AttributeError:
            pass
        self.active_widgets = []

        for final in finals:
            for key, value in final.items():
                if key == "language":
                    self.active_widgets.append(
                        LingmoChoiceEntry(
                            _("Language"), value, "preferences-desktop-locale-symbolic"
                        )
                    )
                elif key == "keyboard":
                    self.active_widgets.append(
                        LingmoChoiceEntry(
                            _("Keyboard"), value["layout"], "input-keyboard-symbolic"
                        )
                    )
                elif key == "timezone":
                    self.active_widgets.append(
                        LingmoChoiceEntry(
                            _("Timezone"),
                            f"{value['region']} {value['zone']}",
                            "preferences-system-time-symbolic",
                        )
                    )
                elif key == "users":
                    self.active_widgets.append(
                        LingmoChoiceEntry(
                            _("Users"),
                            f"{value['username']} ({value['fullname']})",
                            "system-users-symbolic",
                        )
                    )
                elif key == "disk":
                    if "auto" in value:
                        self.active_widgets.append(
                            LingmoChoiceEntry(
                                _("Disk"),
                                f"{value['auto']['disk']} ({value['auto']['pretty_size']})",
                                "drive-harddisk-system-symbolic",
                            )
                        )
                    else:
                        disks = {}
                        # block, device_block
                        for part, info in value.items():
                            part_disk = re.match(
                                "^/dev/[a-zA-Z]+([0-9]+[a-z][0-9]+)?",
                                part,
                                re.MULTILINE,
                            )[0]
                            if part_disk not in disks:
                                disks[part_disk] = LingmoChoiceExpanderEntry(
                                    _("Disk"),
                                    part_disk,
                                    "drive-harddisk-system-symbolic",
                                )
                                self.active_widgets.append(disks[part_disk])

                            disks[part_disk].add_row(
                                LingmoChoiceEntry(
                                    part,
                                    f"{info['fs']} {info['mp']} ({info['pretty_size']})",
                                    "drive-harddisk-system-symbolic",
                                )
                            )

        for widget in self.active_widgets:
            self.group_changes.add(widget)

        self._btn_confirm_signal = self.btn_confirm.connect(
            "clicked", self.__on_confirm
        )

    def __on_confirm(self, widget):
        self.emit("installation-confirmed")
        self.btn_confirm.disconnect(self._btn_confirm_signal)
