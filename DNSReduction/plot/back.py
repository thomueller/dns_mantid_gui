class DNSElasticSCPlotView(DNSView):


    def disconnect_ylim_change(self):
        if hasattr(self, 'cid'):
            self.ax.callbacks.disconnect(self.cid)

    def connect_ylim_change(self):
        self.cid = self.ax.callbacks.connect('ylim_changed',
                                             self.change_cb_range_on_zoom)

    def handle_zoom_settings(self):
        if self.manual_xy and self.axis_type['zoom']['fix_xy']:
            self.lim_changed(draw=False)
        elif self.axis_type['zoom']['fix_xy']:
            self.set_xy_lim()
        if self.axis_type['zoom']['fix_z']:
            self.set_zlim()

    def switch_axis(self, switch):
        if switch:  # switch x and y axes
            self.plotx, self.ploty = self.ploty, self.plotx
            self.plotx = np.transpose(self.plotx)
            self.ploty = np.transpose(self.ploty)
            self.plotz = np.transpose(self.plotz)

    def change_cb_range_on_zoom(self, info=None, draw=True):
        self.manual_xy = False
        state = self.get_state()
        self.projections = state['projections']
        if not self.hasplot:
            return
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        zmap, zmin, zmax, pzmin = filter_z_mesh(self.plotz, xlim, ylim,
                                                self.plotx, self.ploty)
        self.xlim = xlim
        self.ylim = ylim
        if state['log_scale']:
            zmin = pzmin
        if self.manual_z:
            zmin = self.zmin
            zmax = self.zmax
        else:
            self.zmin = zmin
            self.zmax = zmax
        self.pm.set_clim(zmin, zmax)
        if self.projections:
            self.toggle_projections()
        # self.canvas.figure.tight_layout(pad=0.3)
        # yapf: disable
        if ((self.manual_z and isinstance(self.sender(), QAction)) or
            (state['log_scale'] and isinstance(self.sender(), QAction))):
            self.colorbar.remove()
            self.create_colorbar()
            self.canvas.draw()
            # this is quite bad I have no idea why but the colorbar gets tiny
            # if you set limits manually and then zoom and
            # click home button to outzzom
        # yapf: enable

