# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eoyilmaz\Documents\development\anima\anima\ui\ui_files\time_log_dialog.ui'
#
# Created: Wed Feb 08 13:23:23 2017
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(343, 546)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.tasks_label = QtGui.QLabel(Dialog)
        self.tasks_label.setObjectName("tasks_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.tasks_label)
        self.tasks_comboBox = QtGui.QComboBox(Dialog)
        self.tasks_comboBox.setObjectName("tasks_comboBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.tasks_comboBox)
        self.task_progressBar = QtGui.QProgressBar(Dialog)
        self.task_progressBar.setProperty("value", 24)
        self.task_progressBar.setObjectName("task_progressBar")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.task_progressBar)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.resource_comboBox = QtGui.QComboBox(Dialog)
        self.resource_comboBox.setObjectName("resource_comboBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.resource_comboBox)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.calendarWidget = QtGui.QCalendarWidget(Dialog)
        self.calendarWidget.setObjectName("calendarWidget")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.calendarWidget)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label)
        self.start_timeEdit = QtGui.QTimeEdit(Dialog)
        self.start_timeEdit.setTime(QtCore.QTime(10, 0, 0))
        self.start_timeEdit.setCurrentSection(QtGui.QDateTimeEdit.MinuteSection)
        self.start_timeEdit.setCalendarPopup(True)
        self.start_timeEdit.setObjectName("start_timeEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.start_timeEdit)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_2)
        self.end_timeEdit = QtGui.QTimeEdit(Dialog)
        self.end_timeEdit.setTime(QtCore.QTime(19, 0, 0))
        self.end_timeEdit.setCurrentSection(QtGui.QDateTimeEdit.MinuteSection)
        self.end_timeEdit.setCalendarPopup(True)
        self.end_timeEdit.setObjectName("end_timeEdit")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.end_timeEdit)
        self.info_area_label = QtGui.QLabel(Dialog)
        self.info_area_label.setObjectName("info_area_label")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.info_area_label)
        self.revision_label = QtGui.QLabel(Dialog)
        self.revision_label.setObjectName("revision_label")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.revision_label)
        self.revision_type_comboBox = QtGui.QComboBox(Dialog)
        self.revision_type_comboBox.setObjectName("revision_type_comboBox")
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.revision_type_comboBox)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_7)
        self.description_plainTextEdit = QtGui.QPlainTextEdit(Dialog)
        self.description_plainTextEdit.setObjectName("description_plainTextEdit")
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.description_plainTextEdit)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_9)
        self.not_finished_yet_radioButton = QtGui.QRadioButton(Dialog)
        self.not_finished_yet_radioButton.setChecked(True)
        self.not_finished_yet_radioButton.setObjectName("not_finished_yet_radioButton")
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.not_finished_yet_radioButton)
        self.set_as_complete_radioButton = QtGui.QRadioButton(Dialog)
        self.set_as_complete_radioButton.setObjectName("set_as_complete_radioButton")
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.set_as_complete_radioButton)
        self.submit_for_final_review_radioButton = QtGui.QRadioButton(Dialog)
        self.submit_for_final_review_radioButton.setObjectName("submit_for_final_review_radioButton")
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.submit_for_final_review_radioButton)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.tasks_label.setText(QtGui.QApplication.translate("Dialog", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Resource", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.start_timeEdit.setDisplayFormat(QtGui.QApplication.translate("Dialog", "HH:mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.end_timeEdit.setDisplayFormat(QtGui.QApplication.translate("Dialog", "HH:mm", None, QtGui.QApplication.UnicodeUTF8))
        self.info_area_label.setText(QtGui.QApplication.translate("Dialog", "INFO", None, QtGui.QApplication.UnicodeUTF8))
        self.revision_label.setText(QtGui.QApplication.translate("Dialog", "<html><head/><body><p align=\"right\">Revision<br/>Type</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.not_finished_yet_radioButton.setText(QtGui.QApplication.translate("Dialog", "Not Finished Yet", None, QtGui.QApplication.UnicodeUTF8))
        self.set_as_complete_radioButton.setText(QtGui.QApplication.translate("Dialog", "Set As Complete", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_for_final_review_radioButton.setText(QtGui.QApplication.translate("Dialog", "Submit For Final Review", None, QtGui.QApplication.UnicodeUTF8))

