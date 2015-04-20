#
#    Copyright (C) 2014  Jonathan Finlay <jfinlay@riseup.net>
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
"""
The patient visit module
========================

Implements the classes:

* Visit: Main visit module
* ConsultingRoom: Consultings room module

"""

from openerp.osv import osv, fields

class Visit(osv.osv):
    """
    The visit module
    """
    _name = 'visit'
    _description = 'The visit module'

    _states = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('assisted', 'Assisted'),
    ]

    def _default_room(self, cr, uid, id, context=None):
        consulroom_obj = self.pool.get('consulting.room')
        room = consulroom_obj.search(cr, uid, [('default', '=', '1')])
        if room:
            return room[0]
        return 1

    def check_duration(self, cr, uid, id, context=None):
        """
        Check the consistency of the visit duration
        :param cr:
        :param uid:
        :param id:
        :param context:
        :return:
        """
        return {}

    def onchange_consulting_room(self, cr, uid, id, consulting_room, context=None):
        """

        :param cr:
        :param uid:
        :param id:
        :param starts:
        :param consulting_room:
        :param context:
        :return:
        """
        if consulting_room:
            consulroom_obj = self.pool.get('consulting.room')
            duration = consulroom_obj.browse(cr, uid, consulting_room, context=context)[0].duration
        else:
            duration = 0.0

        vals = {
            'value': {
                'duration': duration,
            }
        }
        return vals

    _columns = {
        'name': fields.char('Identifier'),
        'starts': fields.datetime('Start date'),
        'duration': fields.float('Duration',
                                 help='Duration in minutes'),
        'patient_id': fields.many2one('patient', 'Patient'),
        'consultingroom_id': fields.many2one('consulting.room',
                                              'Consulting room'),
        'state': fields.selection(_states, 'State')
    }

    _defaults = {
        'consultingroom_id': _default_room,
    }


class ConsultingRoom(osv.osv):
    """ Consulting rooms """
    _name = 'consulting.room'
    _description = 'Consulting rooms configuration module'

    _columns = {
        'name': fields.char('Name'),
        'duration': fields.float('Standard duration',
                                   help='Visit standard duration time in minutes'),
        'price': fields.float('Price',
                              help='Standard consultation fee'),
        'address': fields.text('Address'),
        'default': fields.boolean('Default', help='Set as default consulting room'),
    }
