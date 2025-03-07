from apps.helper import Log
from apps.schemas import BaseResponse
from apps.schemas.SchemaCIF import RequestCIF, ResponseCIF
from apps.schemas.SchemaLoan import RequestLoan, ResponseLoan, CreateLoan, EditLoan
from apps.helper.ConfigHelper import encoder_app
from main import PARAMS
from apps.models.NewLoanModel import NewLoan
SALT = PARAMS.SALT.salt

class ControllerAris(object):
    @classmethod
    def get_loan_by_cif(cls, input_data=None):
        input_data = RequestCIF(**input_data)
        result = BaseResponse()
        result.status = 400

        try:
            if input_data.cif is not None:
                data = NewLoan.where('cif', '=', input_data.cif).get().serialize()
                if not data:
                    e = "cif not found!"
                    Log.error(e)
                    result.status = 404
                    result.message = str(e)
                else :
                    result.status = 200
                    result.message = "Success"
                    result.data = encoder_app(ResponseCIF(**{"cif_list": data}).json(), SALT)
                    Log.info(result.message)
            else:
                e = "cif not found!"
                Log.error(e)
                result.status = 404
                result.message = str(e)
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    @classmethod
    def get_loan_by_cif_debug(cls, input_data=None):
        input_data = RequestCIF(**input_data)
        result = BaseResponse()
        result.status = 400

        try:
            if input_data.cif is not None:
                data = NewLoan.where('cif', '=', input_data.cif).get().serialize()
                if not data:
                    e = "cif not found!"
                    Log.error(e)
                    result.status = 404
                    result.message = str(e)
                else:
                    result.status = 200
                    result.message = "Success"
                    result.data = ResponseCIF(**{"cif_list": data})
                    Log.info(result.message)
            else:
                e = "cif not found!"
                Log.error(e)
                result.status = 404
                result.message = str(e)
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    @classmethod
    def index_loan(cls):
        result = BaseResponse()
        result.status = 400
        try:
            data = NewLoan.limit(10).get().serialize()
            result.status = 200
            result.message = "Success"
            result.data = ResponseLoan(**{"loan_list": data})
            Log.info(result.message)

        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    @classmethod
    def store_loan(cls, input_data=None):
        input_loan = CreateLoan(**input_data)
        result = BaseResponse()
        result.status = 400

        try:
            loan = NewLoan()

            loan.loanid = input_loan.loanid,
            loan.loan_type = input_loan.loan_type,
            loan.loan_status = input_loan.loan_status,
            loan.loan_amount = input_loan.loan_amount,
            loan.loan_tenure = input_loan.loan_tenure,
            loan.interest = input_loan.interest,
            loan.cif = input_loan.cif

            loan.save()

            # NewLoan.store_loans(input_loan)

            result.status = 200
            result.message = "Success"

        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    @classmethod
    def edit_loan(cls, id: int, input_data=None):
        input_loan = EditLoan(**input_data)
        result = BaseResponse()
        result.status = 400

        try:
            loan = NewLoan.find(id)

            loan.loan_type = input_loan.loan_type,
            loan.loan_status = input_loan.loan_status,
            loan.loan_amount = input_loan.loan_amount,
            loan.loan_tenure = input_loan.loan_tenure,
            loan.interest = input_loan.interest,
            loan.cif = input_loan.cif

            loan.save()

            # NewLoan.store_loans(input_loan)

            result.status = 200
            result.message = "Success"

        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    @classmethod
    def show_loan(cls, id: int):
        result = BaseResponse()
        result.status = 400

        try:
            if id is not None:
                data = NewLoan.where('loanid', '=', id).get().serialize()
                if not data:
                    e = "loan not found!"
                    Log.error(e)
                    result.status = 404
                    result.message = str(e)
                else:
                    result.status = 200
                    result.message = "Success"
                    result.data = ResponseLoan(**{"loan_list": data})
                    Log.info(result.message)
            else:
                e = "loan not found!"
                Log.error(e)
                result.status = 404
                result.message = str(e)
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result

    @classmethod
    def delete_loan(cls, id: int):
        result = BaseResponse()
        result.status = 400

        try:
            if id is not None:
                loan = NewLoan.find(id)
                loan.delete()
                result.status = 200
                result.message = "Success"

            else:
                e = "loan not found!"
                Log.error(e)
                result.status = 404
                result.message = str(e)
        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)

        return result