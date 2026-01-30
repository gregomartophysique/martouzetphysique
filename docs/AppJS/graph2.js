class Line {
    static color(i) {
        var color_liste = ['#1f77b4', "#ff7f0e"];
        return color_liste[i]
    }

    constructor(config) {
        this.config = {
            label: 'Courbe',
            backgroundColor: Line.color(0),
            borderColor: Line.color(0),
            borderWidth: '1px',
            pointRadius: 0,
        };

        this.config = { ...this.config, ...config };
    }

    set_config(config) {
        this.config = { ...this.config, ...config };
    }


}

class Axis {
    constructor( ctx ) {
        this.ctx = ctx;
        //this.chart = new Chart(ctx, {});
        this.lines = [];

        this.config = {
            type: 'line',       // type de graphisme ligne
            options: {
                animation: false,
                animations: { colors: false, x: false, y: false },
                transitions: {
                    active: { animation: false }, resize: { animation: false }
                },
                plugins: {
                    legend: {
                        labels: {
                            usePointStyle: true,
                        },
                    },
                    tooltip: {
                        enabled: false // Pas de bulle
                    },
                },          // fin des plugins
                responsive: true, //false, // permet de s'adapter à la page
                maintainAspectRatio: false,
                scales: {           // les axes
                    x: {                // Axe X
                        type: 'linear',
                        min: 0, max: 5,
                    },  // fin de l'axe X
                    y: { min: 0, max: 1.5,  }   //fin de l'axe Y

                } //fin des axes
            }   // fin des options
        };  //fin de config 
    }

    addLine(line) {
        this.lines.push(line);
    }

    update() {
        this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
        this.ctx.beginPath();
        this.ctx.strokeStyle = "rgb(0,0,0)";
        this.ctx.rect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
        this.ctx.stroke();

        this.ctx.save();
        this.ctx.beginPath();
        this.ctx.font = "20px serif";
        this.ctx.textAlign = "center";
        this.ctx.textBaseline = "bottom";
        this.ctx.fillText("Hello", this.ctx.canvas.width/2, this.ctx.canvas.height/2);
        this.ctx.stroke();
        this.ctx.restore();
        
        let lines_config = [];
        for (let l of this.lines) {
           
            lines_config.push(l.config);
        }

        this.config = { ...this.config, data: { datasets: lines_config } };
        
        //this.chart = new Chart(this.ctx, this.config);
    }

    setxlim( xlim ) {
        this.config.options.scales.x = { ...this.config.options.scales.x, ...xlim };
    }

    setylim(ylim) {
        this.config.options.scales.y = { ...this.config.options.scales.y, ...ylim };
    }

}

class Figure {
    constructor() {
        this.axis = [];
    }

    addAxis(axis) {
        this.axis.push(axis);
    }

    add_line() {
        // Ajout d'un ligne
    }

    update() {
        for (let ax of this.axis) {
            ax.update();
        }
    }


}



class Slider {
    constructor(rangeId, labelId, update_fct, config) {
        this.range = document.getElementById(rangeId);
        this.label = document.getElementById(labelId);
        this.config = { before: "", after: "", fixed: 2, fct_eval: (x) => x, ...config };
        this.update_fct = update_fct;
        this.range.addEventListener('input', () => this.update(), false);

        this.update_value();
    }

    get() {
        return this.value;
    }

    update_value() {
        this.value = this.config.fct_eval(parseFloat(this.range.value.replace(",", ".")));
        this.label.textContent = this.config.before + this.value.toFixed(this.config.fixed) + this.config.after;
        renderMathInElement(this.label);
    }

    update() {
        this.update_value();
        this.update_fct();
    }
}


class Np {
    static linspace(xmin, xmax, nb_pts) {
        let dx = (xmax - xmin) / (nb_pts - 1);
        const x = [];
        for (let i = 0; i < nb_pts; i++) {
            x.push( xmin+ i*dx );
        }
        return x;
    }

    static logspace(xmin, xmax, nb_pts) {
        let dx = (xmax - xmin) / (nb_pts - 1);
        const x = [];
        for (let i = 0; i < nb_pts; i++) {
            x.push( 10**(xmin + i * dx) );
        }
        return x;
    }


    static toObject(x, y) {
        const data = [];
        for (let i = 0; i < x.length; i++) {
            data.push({ x: x[i], y: y[i] } )
        }
        return data;
    }
}

class GTick {
	constructor(ctx, value, { textAlign = 'right', textBaseline = 'middle', font = '18px serif' } = {}) {
		this.value = value;
		this._ctx = ctx;
		this.fixed = 1;

		this.style = {
			font: font,
			textAlign: textAlign,
			textBaseline: textBaseline
		};

		this.update();
	}

	update() { // Calcul des grandeurs
		this._ctx.save();
		this._ctx.font = this.style.font;
		this._ctx.textAlign = this.style.textAlign;
		this._ctx.textBaseline = this.style.textBaseline;
		var metrics = this._ctx.measureText(this.value.toFixed(this.fixed));
		this._ctx.restore();
		this.width = metrics.width;
		this.heigth = metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent;
	}

	draw(x, y) {
		this._ctx.save();
		this._ctx.beginPath();
		this._ctx.font = this.style.font;
		this._ctx.textAlign = this.style.textAlign;
		this._ctx.textBaseline = this.style.textBaseline;

		this._ctx.fillText( this.value.toFixed(1), x, y);

		this._ctx.stroke();
		this._ctx.restore();
	}
}

class GTicks {
	constructor(ctx, { min = 0, max = 1, num = 5, textAlign = 'right', textBaseline = 'middle', font = '24px serif' } = {}) {
		this._ctx = ctx;
		this.min = min;
		this.max = max;
		this.num = num;

		this.fixed = 1;

		var value = Np.linspace(this.min, this.max, num);

		this.ticks = [];
		for (let i = 0; i < value.length; i++) {
			this.ticks.push(new GTick(ctx, value[i], textAlign = textAlign, textBaseline = textBaseline, font = font) )
		}
	}

	set(min = 0, max = 1) {
		this.min = min;
		this.max = max;

		var value = Np.linspace(this.min, this.max, this.num);

		this.ticks = [];
		for (let i = 0; i < value.length; i++) {
			this.ticks.push(new GTick(this._ctx, value[i]))
		}
	}

	maxHeight() {
		var max_height = 0;
		for (let i = 0; i < this.ticks.length; i++) {
			var height = this.ticks[i].height;
			if (height > max_height) {
				max_height = height;
			};
		}
		return max_height;
	}

	

	maxWidth() {
		var max_width = 0;
		for (let i = 0; i < this.ticks.length; i++) {
			var width = this.ticks[i].width;
			if (width > max_width) {
				max_width = width;
			};
		}
		return max_width;
	}

	last() {
		return this.ticks[this.ticks.length];
	}



	draw() {

	}

}

class GAxis {
	constructor(ctx) {
		this._ctx = ctx; 
		
		this.aspect_equal = false;

		this.xticks = new GTicks(ctx, { textAlign:'center' });
		this.yticks = new GTicks(ctx);

		this.update_bbox();
		this.drawAxe();
	}

	set_xlim(xmin, xmax) { this.xticks.set(xmin, xmax); this.update_bbox(); this.drawAxe(); }
	set_ylim(ymin, ymax) { this.yticks.set(ymin, ymax); this.update_bbox(); this.drawAxe(); }

	update() {
		this.update_bbox();
		this.drawAxe();
	}

	update_bbox() {
		// vérification de l'aspect-ratio
		if (this.aspect_equal) {
			var f = this._ctx.canvas.height / (this._xylim.ymax - this._xylim.ymin);
			var f2 = this._ctx.canvas.width / (this._xylim.xmax - this._xylim.xmin);
			this._xylim.xmin = this._xylim.xmin * f2 / f;
			this._xylim.xmax = this._xylim.xmax * f2 / f;
		}

		// Tailles des ticks - graduations X
		// Tailles des ticks - graduations X
		var max_height = this.xticks.maxHeight();

		// Tailles des ticks - graduations Y
		var max_width = this.yticks.maxWidth();


		
		var x0 = 5 + max_width;
		var y0 = 5;
		var pdx = 5;
		var pdy = 5;
		var w = this._ctx.canvas.width - x0 - pdx;
		var h = this._ctx.canvas.height - y0 - pdy - max_height;

		this._bbox = {
			width: w,
			height: h,
			h: h,
			w: w,
			pdx: pdx,
			pdy: pdy,
			x0: x0,
			y0: y0
		}
	}

	drawxtick() { // Graduations X
		if (this._showXticks == false) { return; }
		for (let i = 0; i < this.xticks.num; i++) {
			var pt = this.convertXY(this.xticks.ticks[i].value, 0);
			this.xticks.ticks[i].draw(pt.x, this._bbox.y0 + this._bbox.h + 5);
		}
	}

	drawytick() { // Graduations Y
		if (this._showYticks == false) { return; }
		//this._ctx.textAlign = "right";
		//this._ctx.textBaseline = "middle";
		for (let i = 0; i < this.yticks.num; i++) {
			var pt = this.convertXY(0, this.yticks.ticks[i].value );
			this.yticks.ticks[i].draw(this._bbox.x0, pt.y); 
		}
		
	}

	drawxgrid() { // Grille X
		if (this._showXgrid == false) { return; }
		for (let i = 0; i < this.xticks.length; i++) {
			this.drawLine(this.xticks[i], this._xylim.ymin, this.xticks[i], this._xylim.ymax, this.xgridstyle);
		}
	}

	drawygrid() { // Grille Y
		if (this._showYgrid == false) { return; }
		for (let i = 0; i < this.yticks.length; i++) {
			this.drawLine(this._xylim.xmin, this.yticks[i], this._xylim.xmax, this.yticks[i], this.ygridstyle);
		}
	}

	drawAxe() {
		// Clear
		this._ctx.clearRect(0, 0, this._ctx.canvas.width, this._ctx.canvas.height);

		// Cadre
		this._ctx.beginPath();
		this._ctx.strokeStyle = "rgb(0,0,0)";
		this._ctx.rect(this._bbox.x0, this._bbox.y0, this._bbox.w, this._bbox.h);
		this._ctx.stroke();

		this.drawxtick();
		this.drawxgrid();
		this.drawytick();
		this.drawygrid();

		// Affichage axe centrale (passe par 0)
		if (this._show_central_line) {
			//this.drawLine(0, this._xylim.ymin, 0, this._xylim.ymax);
			//this.drawLine(this._xylim.xmin, 0, this._xylim.xmax, 0);
		}
	}

	drawLine(x1, y1, x2, y2, style = "rgb(0,0,0)") {
		var pt1 = this.convertXY(x1, y1);
		var pt2 = this.convertXY(x2, y2);
		this._ctx.save();
		this._ctx.beginPath();
		this._ctx.strokeStyle = style;
		this._ctx.moveTo(pt1.x, pt1.y);
		this._ctx.lineTo(pt2.x, pt2.y);
		this._ctx.stroke();
		this._ctx.restore();
	}

	moveTo(x, y) {
		var pt = this.convertXY(x, y);
		this._ctx.moveTo(pt.x, pt.y);
	}

	lineTo(x, y) {
		var pt = this.convertXY(x, y);
		this._ctx.lineTo(pt.x, pt.y);
	}

	convertXY(x, y) {
		var xmin = this.xticks.min;
		var xmax = this.xticks.max;
		var ymin = this.yticks.min;
		var ymax = this.yticks.max;
		var width = this._bbox.width;
		var height = this._bbox.height;
		return {
			x: (x - xmin) * width / (xmax - xmin) + this._bbox.x0,
			y: height - (y - ymin) * height / (ymax - ymin) + this._bbox.y0,
		}
	}

	plot(fct, xmin, xmax, dx = 0.1) {
		xmin = typeof xmin !== "undefined" ? xmin : xmin = this._xylim.xmin;
		xmax = typeof xmax !== "undefined" ? xmax : xmax = this._xylim.xmax;

		if (xmin < this._xylim.xmin) { xmin = this._xylim.xmin; };
		if (xmax > this._xylim.xmax) { xmax = this._xylim.xmax; };

		this._ctx.save();
		this._ctx.beginPath();
		this._ctx.lineWidth = 2;
		this._ctx.strokeStyle = "rgb(66,44,255)";

		var x = xmin;
		var y = fct(x);
		var pt = this.convertXY(x, y);
		this._ctx.moveTo(pt.x, pt.y);
		while (x < xmax) {
			x += dx;
			y = fct(x);
			pt = this.convertXY(x, y);
			this._ctx.lineTo(pt.x, pt.y);
		}
		this._ctx.stroke();
		this._ctx.restore();

	}
}