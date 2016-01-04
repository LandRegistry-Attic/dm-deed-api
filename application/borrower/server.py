from application.borrower.model import Borrower


class BorrowerService:
    def saveBorrower(self, borrower, id=None):
        borrowerModel = Borrower()
        if id is not None:
            borrowerModel.id = id

        borrowerModel.forename = borrower['forename']

        if 'middle_name' in borrower:
            borrowerModel.middlename = borrower['middle_name']

        borrowerModel.surname = borrower['surname']
        borrowerModel.dob = borrower['dob']

        if 'gender' in borrower:
            borrowerModel.gender = borrower['gender']

        borrowerModel.phonenumber = borrower['phone_number']
        borrowerModel.address = borrower['address']

        if id is not None:
            borrowerModel.update()
        else:
            borrowerModel.save()

        return borrowerModel.id
