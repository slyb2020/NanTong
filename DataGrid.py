import wx
import wx.grid as gridlib
from DBOperation import GetAllOrderList,GetOrderDetailRecord
from OrderDetailTree import OrderDetailTree
from ID_DEFINE import *
import numpy as np
import images
import copy

class DataGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent, data,titleList,colSizeList, log=None):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.moveTo = None
        self.data = data
        self.titleList = titleList
        self.colSizeList = colSizeList
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.CreateGrid(self.data.shape[0], self.data.shape[1])#, gridlib.Grid.SelectRows)
        for i in range(self.data.shape[1]):
            self.SetColLabelSize(25)
            self.SetColSize(i, self.colSizeList[i])
            self.SetColLabelValue(i,self.titleList[i])
        for rowNum,row in enumerate(self.data):
            self.SetRowLabelSize(40)
            self.SetRowLabelValue(rowNum,str(rowNum+1))
            for colNum,col in enumerate(row):
                self.SetCellAlignment(rowNum,colNum,wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
                self.SetCellValue(rowNum,colNum,str(col))
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnGridColSort)
        self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)


    def OnCellLeftClick(self, evt):
        row = evt.GetRow()
        self.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.SelectRow(row)
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        evt.Skip()

    def OnGridColSort(self, evt):
        self.log.write("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())

    def OnRowSize(self, evt):
        evt.Skip()

    def OnColSize(self, evt):
        evt.Skip()

    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        evt.Skip()
