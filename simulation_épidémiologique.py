from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
from matplotlib.animation import FuncAnimation
import subprocess
import sys

try:
    import pyinputplus as pyip
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyinputplus'])
finally:
    import pyinputplus as pyip

plt.style.use("ggplot")

N = 500000

# Sélection du modèle
model_selection = pyip.inputMenu(["SIR", "SEIR"], prompt = "Veuillez choisir l'un des modèles suivant:\n")

if model_selection == "SIR":
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (11, 8))
    ax1.set(xlim = (0, 100), ylim = (-0.01, 1.01))

    ax2=plt.subplot(2, 1, 2)
    ax2.axis('off')
    ax2.set_title('Paramètres du modèle SIR', y = 0.4)
    axis_color = 'lightgoldenrodyellow'

    # Création des sliders
    E0_slider_ax = fig.add_axes([0.30, .22, 0.3, 0.02], facecolor = axis_color)
    E1_slider_ax = fig.add_axes([0.30, .17, 0.3, 0.02], facecolor = axis_color)
    E2_slider_ax = fig.add_axes([0.30, .12, 0.3, 0.02], facecolor = axis_color)
    E0_slider = Slider(E0_slider_ax, r'Distanciation Sociale ($\mu$)', valmin = 0, valmax = 0.3, valinit = 0, valstep = 0.1)
    E0_slider.label.set_size(15)
    E1_slider = Slider(E1_slider_ax, r"Période d'infectivité (jours)", valmin = 0, valmax = 10, valinit = 1, valstep = 0.5)
    E1_slider.label.set_size(15)
    E2_slider = Slider(E2_slider_ax, r"$R_{0}$", valinit = 1.5, valmin = 1.0, valmax = 10, valstep = 0.5)
    E2_slider.label.set_size(15)

    line1, = ax1.plot([], [], color = "blue", lw = 3, label = "Susceptibles")
    line2, = ax1.plot([], [], color = "red", lw = 3, label = "Infected")
    line3, = ax1.plot([], [], color = "green", lw = 3, label = "Recovered")

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    def animate_sir(num):
        u = E0_slider.val
        t_infective = E1_slider.val
        R0 = E2_slider.val

        gamma = 1/t_infective
        beta = R0 * gamma

        sir_i0 = 1 / N
        sir_r0 = 0.00
        sir_s0 = 1 - sir_i0 - sir_r0

        x0_sir = [sir_s0, sir_i0, sir_r0]

        def sir(x, t):
            s, i, r = x
            dx = np.zeros(3)
            dx[0] = -(1 - u) * beta * s * i
            dx[1] = (1 - u) * (beta * s * i) - gamma * i
            dx[2] = gamma * i
            return dx

        t = np.linspace(0, 150, 150)
        sir_ode = odeint(sir, x0_sir, t)
        s = sir_ode[:, 0]; i = sir_ode[:, 1]; r = sir_ode[:, 2]

        line1.set_data(t[:num], s[:num])
        line2.set_data(t[:num], i[:num])
        line3.set_data(t[:num], r[:num])
        ax1.legend(loc = "lower center", bbox_to_anchor = (0.5, -0.35), ncol = 3)
        add_text = "\n".join(("Paramètres:",
                              r"$\beta = %.2f$" % (beta,),
                              r"$\gamma = %.2f$" % (gamma,)))
        fig.text(1.1, 0.5, add_text, transform = ax1.transAxes, fontsize = 14, bbox = props)
        fig.subplots_adjust(left = 0.1, right = 0.7, bottom = 0.2)
        ax1.set_title("Courbe SIR", fontsize=20, fontweight="bold")
        ax1.set_xlabel("Temps (jours)")
        ax1.set_ylabel("Proportion de la Population")

        return line1, line2, line3,

    def animate_button(self):
        t = np.linspace(0, 150, 150)
        anim = FuncAnimation(fig, animate_sir, frames=len(t) + 1, interval = 50, blit = True, repeat = False)
        fig.canvas.draw()

    axnext = fig.add_axes([0.785, 0.1, 0.12, 0.12], facecolor = axis_color, frameon = True)
    bnext = Button(axnext, 'Modéliser', color = "grey", hovercolor='0.90')
    bnext.on_clicked(animate_button)

    plt.show()

elif model_selection == "SEIR":
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 8))
    ax1.set(xlim = (0, 150), ylim = (-0.01, 1.01))

    ax2=plt.subplot(2, 1, 2)
    ax2.axis('off')
    ax2.set_title('Paramètres du modèle SEIR', y = 0.4, fontweight="bold")
    axis_color = 'lightgoldenrodyellow'

    E0_slider_ax = fig.add_axes([0.30, .22, 0.3, 0.02], facecolor = axis_color)
    E1_slider_ax = fig.add_axes([0.30, .17, 0.3, 0.02], facecolor = axis_color)
    E2_slider_ax = fig.add_axes([0.30, .12, 0.3, 0.02], facecolor = axis_color)
    E3_slider_ax = fig.add_axes([0.30, .07, 0.3, 0.02], facecolor = axis_color)

    E0_slider = Slider(E0_slider_ax, r'Distanciation Sociale ($\mu$)', valmin = 0, valmax = 0.3, valinit = 0, valstep = 0.1)
    E0_slider.label.set_size(15)
    E1_slider = Slider(E1_slider_ax, r"Période d'infectivité (jours)", valmin = 0, valmax = 10, valinit = 1, valstep = 0.5)
    E1_slider.label.set_size(15)
    E2_slider = Slider(E2_slider_ax, r"Période d'incubation (jours)", valmin = 0, valmax = 10, valinit = 1, valstep = 0.5)
    E2_slider.label.set_size(15)
    E3_slider = Slider(E3_slider_ax, r"$R_{0}$", valinit = 1.5, valmin = 1, valmax = 10, valstep = 0.5)
    E3_slider.label.set_size(15)

    line1, = ax1.plot([], [], color = "blue", lw = 3, label = "Susceptibles")
    line2, = ax1.plot([], [], color = "purple", lw = 3, label = "Exposed")
    line3, = ax1.plot([], [], color = "red", lw = 3, label = "Infected")
    line4, = ax1.plot([], [], color = "green", lw = 3, label = "Recovered")

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    def animate_seir(num):
        u = E0_slider.val
        t_infective = E1_slider.val
        t_incubation = E2_slider.val
        R0 = E3_slider.val

        alpha = 1/t_incubation
        gamma = 1/t_infective
        beta = R0 * gamma

        seir_e0 = 1 / N
        seir_i0 = 0.00
        seir_r0 = 0.00
        seir_s0 = 1 - seir_e0 - seir_i0 - seir_r0

        x0_seir = [seir_s0, seir_e0, seir_i0, seir_r0]

        def seir(x, t):
            s, e, i, r = x
            dx = np.zeros(4)
            dx[0] = -(1 - u) * beta * s * i
            dx[1] = (1 - u) * beta * s * i - alpha * e
            dx[2] = alpha * e - gamma * i
            dx[3] = gamma * i
            return dx

        t = np.linspace(0, 201, 200)
        seir_ode = odeint(seir, x0_seir, t)
        s = seir_ode[:, 0]; e = seir_ode[:, 1]; i = seir_ode[:, 2]; r = seir_ode[:, 3]

        line1.set_data(t[:num], s[:num])
        line2.set_data(t[:num], e[:num])
        line3.set_data(t[:num], i[:num])
        line4.set_data(t[:num], r[:num])

        ax1.legend(loc = "lower center", bbox_to_anchor = (0.5, -0.35), ncol = 4)
        add_text = "\n".join(("Paramètres:",
                              r"$\alpha = %.2f$" % (alpha,),
                              r"$\beta = %.2f$" % (beta,),
                              r"$\gamma = %.2f$" % (gamma,)))

        fig.text(1.1, 0.5, add_text, transform = ax1.transAxes, fontsize = 14, bbox = props)
        fig.subplots_adjust(left = 0.1, right = 0.7, bottom = 0.2)
        ax1.set_title("Courbe SEIR", fontsize=20, fontweight="bold")
        ax1.set_xlabel("Temps (jours)")
        ax1.set_ylabel("Proportion de la Population")

        return line1, line2, line3, line4,

    def animate_button(self):
        t = np.linspace(0, 150, 150)
        anim = FuncAnimation(fig, animate_seir, frames=len(t) + 1, interval = 50, blit = True, repeat = False)
        fig.canvas.draw()

    axnext = fig.add_axes([0.75, 0.1, 0.12, 0.12], facecolor = axis_color, frameon = True)
    bnext = Button(axnext, 'Modéliser', color = "grey", hovercolor='0.90')
    bnext.on_clicked(animate_button)

    plt.show()
