from .DBCONNECTION import DBConnection


class LR:
    def validate_login(self, username, password, usertype):
        db = DBConnection()
        query = """\
            DECLARE @out int;
            EXEC [dbo].[Signin] @email= ?,@pass= ?,@type= ?, @flag=@out OUTPUT;
            SELECT @out AS the_output;
            """
        values = (username, password, usertype)
        result = db.executeproc(query, values)
        db.closeConnection()
        return result

    def register(self, username, email, password, DOB, usertype):
        db = DBConnection()
        print(username, password, email, DOB, usertype)
        query = """\
                    DECLARE @out int;
                    EXEC [dbo].[SignUp] @name= ?,@pass= ?,@mail=?,@date=?,@type= ?,@flag=@out OUTPUT;
                    SELECT @out AS the_output;
                    """
        values = (username, password, email, DOB, usertype)
        result = db.executeproc(query, values)
        db.closeConnection()
        return result
