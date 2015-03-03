#
# Copyright (C) 2014  Jonathan Finlay <jfinlay@riseup.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

{
    'name': 'Infosalud - Patient',
    'version': '1.0',
    'author': 'Jonathan Finlay <jfinlay@riseup.net>',
    'category': 'Health',
    'description': """

Infosalud.
==========



Libre Electronic Health Record System:
--------------------------------------
    * Manage patient data
    * Manage diseases


    """,
    'website': 'https://eme.infosalud.org',
    'depends': ['base'],
    'data': [
        'view/patient_view.xml',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
