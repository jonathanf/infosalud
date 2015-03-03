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
The patient module
==================

Implements the classes:

* Patient: Main patient module

"""

from openerp.osv import osv, fields

class Patient(osv.osv):
    """
    The patient main module
    """
    _name = 'patient'
    _description = 'The patient main module'

    _inherits = {
        'res.partner': 'partner_id',
    }

    def _age(self, cr, uid, ids, name, args, context=None):
        """
        Compute patient's age in format ##y ##m (years, months)

        :param ids: list() of patient ids
        :return: str() patient age
        """
        res = {}
        for item in ids:
            age = ''
            cr.execute("SELECT dob, deceased, dod "
                       "FROM patient, res_partner "
                       "WHERE patient.partner_id = res_partner.id"
                       " AND patient.id = '%s';" % item)
            data = cr.fetchone()  # Return tuple(dob, deceased, dod)
            if data[0]:
                import datetime
                from dateutil.relativedelta import relativedelta

                dob = data[0]
                start = datetime.datetime.strptime(dob, '%Y-%m-%d')

                if data[1] and data[2]:
                    ends = datetime.datetime.strptime(data[2], '%Y-%m-%d')
                else:
                    ends = datetime.datetime.now()

                diff = relativedelta(ends, start)
                age = '%sy %sm' % (diff.years, diff.months)
            res = {item: age}
        return res

    def _compose_name(self, cr, uid, ids, context=None):
        """
        Compose a full name of patients ids

        :param cr: pgsql cursor
        :param ids: list() patients record ids
        :return: str() patient full name
        """
        if hasattr(ids, '__iter__'):
            ids = ids[0]
        name = ""
        cr.execute("SELECT \"fatherSurname\", \"motherSurname\", "
                   "\"firstName\", \"middleName\" "
                   "FROM patient "
                   "WHERE id = '%s'" % ids)
        for item in cr.fetchone():
            if item:
                name += item
                name += " "
        if name:
            super(Patient, self).write(cr, uid, ids, {'name': name}, context=context)
            return True
        return False

    _columns = {
        'identifier': fields.char('Identifier'),
        'firstName': fields.char('First name', size=64),
        'middleName': fields.char('Middle name', size=64),
        'fatherSurname': fields.char('Surname', size=64),
        'motherSurname': fields.char('Mother Surname', size=64),
        'dob': fields.date('Date of birth'),
        'deceased': fields.boolean('Decease', help="This is a deceased patient"),
        'dod': fields.date('Date of decease'),
        'age': fields.function(_age, type='char', size=32, string='Age',
                               help="Age of patient represented in years (y) and months (m)",
                               store={}),
        'gender': fields.selection([('1', 'Male'), ('2', 'Female')],
                                   'Sex/Gender'),
        'partner_id': fields.many2one('res.partner', required=True,
                                      string='Related Partner',
                                      ondelete='restrict',
                                      help='Partner-related data of the user',
                                      auto_join=True),
        'personal_history': fields.html('Personal history'),
        'family_history': fields.html('Family history'),
    }

    def create(self, cr, uid, vals, context=None):
        """
        Override osv create method to patient compute full name

        :param vals: dict() with create values
        :return: integer id of new patient record
        """
        vals['name'] = ""
        if 'fatherSurname' in vals and vals['fatherSurname']:
            vals['name'] += vals['fatherSurname']
            vals['name'] += " "
        if 'motherSurname' in vals and vals['motherSurname']:
            vals['name'] += vals['motherSurname']
            vals['name'] += " "
        if 'firstName' in vals and vals['firstName']:
            vals['name'] += vals['firstName']
            vals['name'] += " "
        if 'middleName' in vals and vals['middleName']:
            vals['name'] += vals['middleName']
        return super(Patient, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """
        Override osv write method to compute patient full name

        :param ids: list() patients record ids
        :param vals: dict() with modified fields/values
        :return: integer id of new patient record
        """
        res = super(Patient, self).write(cr, uid, ids, vals, context=context)
        if 'fatherSurname' or 'motherSurname' \
                or 'firstName' or 'middleName' in vals:
            self._compose_name(cr, uid, ids, context=context)
        return res

    _defaults = {
        'patient': True,
        'customer': True,
        'provider': False,
        'employee': False,
    }

    _order = 'identifier asc'
