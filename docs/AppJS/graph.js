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
        this.chart = new Chart(ctx, {});
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
        this.chart.destroy();

        let lines_config = [];
        for (let l of this.lines) {
           
            lines_config.push(l.config);
        }

        this.config = { ...this.config, data: { datasets: lines_config } };
        
        this.chart = new Chart(this.ctx, this.config);
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