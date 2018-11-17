class RawCourseData:
    def __init__(self, data: tuple):
        self.data = data
        self.grade,\
            self.control_number,\
            self.course_number,\
            self.trade,\
            self.section,\
            self.class_,\
            self.group,\
            self.required_or_selective,\
            self.credits,\
            self.field,\
            self.course_name,\
            self.course_remark,\
            self.enrollment_maximum,\
            self.instructor,\
            self.day_hour_classroom,\
            self.department = data

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return '\t'.join((str(e) for e in self.data))
