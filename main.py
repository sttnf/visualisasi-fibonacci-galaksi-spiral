import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

class FibonacciDashboard:
    def __init__(self):
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 9))
        self.setup_layout()
        
        # Konstanta
        self.GOLDEN_RATIO = (1 + np.sqrt(5)) / 2
        self.n_terms = 20
        self.n_stars = 4000
        self.rotation_speed = 0.16
        self.time = 0
        
        # Generate data Fibonacci
        self.initialize_fibonacci_data()
        self.initialize_galaxy_data()
        self.setup_plots()
        
        # Animasi
        self.anim = FuncAnimation(
            self.fig, self.update,
            init_func=self.init_animation,
            frames=None, interval=30, blit=True
        )
    
    def setup_layout(self):
        """Setup layout dashboard"""
        gs = GridSpec(3, 3, figure=self.fig)
        self.ax_galaxy = self.fig.add_subplot(gs[0:2, 0:2])
        self.ax_ratio = self.fig.add_subplot(gs[0, 2])
        self.ax_spiral = self.fig.add_subplot(gs[1, 2])
        self.ax_stats = self.fig.add_subplot(gs[2, :])
        
        self.fig.patch.set_facecolor('#0A0A0A')
        for ax in [self.ax_galaxy, self.ax_ratio, self.ax_spiral, self.ax_stats]:
            ax.set_facecolor('#0A0A0A')
            
    def initialize_fibonacci_data(self):
        """Inisialisasi data Fibonacci dan statistik"""
        # Generate sequence
        self.sequence = [1, 1]
        self.ratios = [1]
        for i in range(2, self.n_terms):
            self.sequence.append(self.sequence[i-1] + self.sequence[i-2])
            self.ratios.append(self.sequence[i] / self.sequence[i-1])
        
        # Statistik
        self.stats_data = {
            'Nilai': self.sequence,
            'Rasio': self.ratios + [self.GOLDEN_RATIO],
            'Log': [np.log(x) for x in self.sequence],
            'Selisih': [0] + [self.sequence[i] - self.sequence[i-1] 
                             for i in range(1, len(self.sequence))]
        }
        
    def initialize_galaxy_data(self):
        """Inisialisasi data galaksi"""
        # Posisi bintang
        self.theta = np.random.uniform(0, 2*np.pi, self.n_stars)
        r_base = np.random.power(0.5, self.n_stars) * 5
        self.r = r_base + np.random.normal(0, 0.2, self.n_stars)
        
        # Kecepatan dan properti
        self.angular_speed = 1 / (self.r + 0.1)**0.5
        brightness = np.random.power(2, self.n_stars)
        
        # Warna bintang
        self.colors = np.zeros((self.n_stars, 3))
        self.colors[:, 0] = 0.8 + 0.2 * brightness  # Red
        self.colors[:, 1] = 0.6 * brightness        # Green
        self.colors[:, 2] = 0.4 + 0.6 * brightness  # Blue
        
        # Ukuran bintang
        self.sizes = np.random.power(2, self.n_stars) * 50
        
    def setup_plots(self):
        """Setup semua plot"""
        # Setup Galaksi
        self.ax_galaxy.set_xlim(-6, 6)
        self.ax_galaxy.set_ylim(-6, 6)
        self.ax_galaxy.axis('off')
        self.ax_galaxy.set_title('Galaksi Fibonacci', color='white', size=14)
        self.scatter = self.ax_galaxy.scatter([], [], c=[], s=[], alpha=0.6)
        
        # Setup Plot Rasio
        self.ax_ratio.set_title('Konvergensi ke Golden Ratio', color='white', size=12)
        self.ax_ratio.grid(True, alpha=0.2)
        self.ax_ratio.axhline(y=self.GOLDEN_RATIO, color='gold', linestyle='--', alpha=0.5)
        self.ratio_line, = self.ax_ratio.plot([], [], 'w-', alpha=0.8)
        self.ratio_dots = self.ax_ratio.scatter([], [], c='cyan', s=50)
        self.ax_ratio.set_ylim(1, 2)
        self.ax_ratio.set_xlim(0, self.n_terms)
        
        # Setup Spiral Fibonacci
        self.ax_spiral.set_title('Spiral Fibonacci', color='white', size=12)
        self.spiral_line, = self.ax_spiral.plot([], [], 'cyan', alpha=0.8)
        self.ax_spiral.set_aspect('equal')
        self.ax_spiral.axis('off')
        
        # Setup Statistik
        self.ax_stats.set_title('Statistik Fibonacci', color='white', size=12)
        self.stats_text = self.ax_stats.text(
            0.02, 0.5, '',
            transform=self.ax_stats.transAxes,
            color='white', fontsize=10,
            verticalalignment='center'
        )
        self.ax_stats.axis('off')
        
        plt.tight_layout()
        
    def generate_spiral_points(self, t):
        """Generate titik-titik spiral Fibonacci"""
        a = 0.5
        r = a * self.fibonacci_spiral(t)
        x = r * np.cos(t)
        y = r * np.sin(t)
        return x, y
        
    def fibonacci_spiral(self, theta):
        """Fungsi spiral Fibonacci"""
        return np.exp(theta / self.GOLDEN_RATIO)
        
    def format_statistics(self, current_idx):
        """Format statistik untuk ditampilkan"""
        stats = []
        
        # Deret terakhir
        last_terms = self.sequence[max(0, current_idx-4):current_idx+1]
        stats.append(f"Deret Terakhir: {' → '.join(map(str, last_terms))}")
        
        # Rasio terakhir
        current_ratio = self.ratios[min(current_idx, len(self.ratios)-1)]
        stats.append(f"Rasio Saat Ini: {current_ratio:.6f}")
        stats.append(f"Golden Ratio (φ): {self.GOLDEN_RATIO:.6f}")
        
        # Properti matematika
        if current_idx > 0:
            growth_rate = (self.sequence[current_idx] / 
                          self.sequence[current_idx-1] - 1) * 100
            stats.append(f"Tingkat Pertumbuhan: {growth_rate:.2f}%")
        
        # Statistik tambahan
        total = sum(self.sequence[:current_idx+1])
        stats.append(f"Jumlah Total: {total:,}")
        
        if current_idx > 1:
            ratio_error = abs(current_ratio - self.GOLDEN_RATIO)
            stats.append(f"Error dari φ: {ratio_error:.6f}")
        
        return "\n".join(stats)
        
    def init_animation(self):
        """Inisialisasi animasi"""
        self.scatter.set_offsets(np.c_[[], []])
        self.ratio_line.set_data([], [])
        self.ratio_dots.set_offsets(np.c_[[], []])
        self.spiral_line.set_data([], [])
        self.stats_text.set_text("")
        return (self.scatter, self.ratio_line, self.ratio_dots,
                self.spiral_line, self.stats_text)
        
    def update(self, frame):
        """Update animasi untuk setiap frame"""
        self.time += self.rotation_speed
        current_idx = int(self.time * 2) % self.n_terms
        
        # Update galaksi
        rotated_theta = self.theta + self.time * self.angular_speed
        r_dynamic = self.r * (1 + 0.1 * np.sin(self.time + rotated_theta))
        x = r_dynamic * np.cos(rotated_theta)
        y = r_dynamic * np.sin(rotated_theta)
        
        dynamic_colors = self.colors.copy()
        dynamic_colors *= (1 + 0.2 * np.sin(self.time + rotated_theta)[:, np.newaxis])
        dynamic_colors = np.clip(dynamic_colors, 0, 1)
        
        dynamic_sizes = self.sizes * (1 + 0.3 * np.sin(self.time + rotated_theta))
        
        self.scatter.set_offsets(np.c_[x, y])
        self.scatter.set_color(dynamic_colors)
        self.scatter.set_sizes(dynamic_sizes)
        
        # Update rasio plot
        x_data = range(1, current_idx + 2)
        y_data = self.ratios[:current_idx + 1]
        self.ratio_line.set_data(x_data, y_data)
        self.ratio_dots.set_offsets(np.c_[x_data, y_data])
        
        # Update spiral
        t = np.linspace(0, current_idx * np.pi/2, 1000)
        spiral_x, spiral_y = self.generate_spiral_points(t)
        self.spiral_line.set_data(spiral_x, spiral_y)
        
        # Update statistik
        self.stats_text.set_text(self.format_statistics(current_idx))
        
        return (self.scatter, self.ratio_line, self.ratio_dots,
                self.spiral_line, self.stats_text)
        
    def show(self):
        """Tampilkan animasi"""
        plt.show()

# Jalankan dashboard
if __name__ == "__main__":
    dashboard = FibonacciDashboard()
    dashboard.show()