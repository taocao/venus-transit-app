import streamlit as st
import numpy as np
import plotly.graph_objs as go
import time

class VenusTransitSimulation:
    def __init__(self):
        # Orbital parameters
        self.earth_radius = 1.0
        self.venus_radius = 0.72
        self.earth_orbital_period = 365.25
        self.venus_orbital_period = 224.7

    def generate_orbital_data(self, time, radius, period):
        """Generate planet position at a given time"""
        angle = (2 * np.pi * time) / period
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        return x, y

    def is_transit_occurring(self, earth_x, earth_y, venus_x, venus_y):
        """Determine if a transit is occurring"""
        # Calculate angular distance between planets
        angular_distance = np.sqrt((earth_x - venus_x)**2 + (earth_y - venus_y)**2)
        
        # Threshold for transit (adjust as needed)
        transit_threshold = 0.15
        
        return angular_distance < transit_threshold

    def create_simulation(self):
        st.title("Venus Transit: Celestial Dynamics 🌞🌍🌕")
        
        # Use placeholders to reduce re-rendering
        time_placeholder = st.empty()
        plot_placeholder = st.empty()
        info_placeholder = st.empty()

        # Session state for animation control
        if 'time' not in st.session_state:
            st.session_state.time = 0
        if 'is_playing' not in st.session_state:
            st.session_state.is_playing = False

        # Control column
        col1, col2, col3 = st.columns(3)
        
        with col1:
            play_button = st.button('▶️ Play')
            if play_button:
                st.session_state.is_playing = True
        
        with col2:
            pause_button = st.button('⏸️ Pause')
            if pause_button:
                st.session_state.is_playing = False
        
        with col3:
            reset_button = st.button('🔄 Reset')
            if reset_button:
                st.session_state.time = 0
                st.session_state.is_playing = False

        # Animation logic
        if st.session_state.is_playing:
            st.session_state.time += 2

        # Simulation parameters
        show_orbits = st.checkbox("Show Orbital Paths", True)
        speed_multiplier = st.slider("Simulation Speed", 0.5, 2.0, 1.0)

        # Create figure
        fig = go.Figure()

        # Sun
        fig.add_trace(go.Scatter(
            x=[0], y=[0], 
            mode='markers',
            marker=dict(color='yellow', size=30, symbol='circle'),
            name='Sun'
        ))

        # Calculate planetary positions with speed multiplier
        earth_x, earth_y = self.generate_orbital_data(
            st.session_state.time * speed_multiplier, 
            self.earth_radius, 
            self.earth_orbital_period
        )
        venus_x, venus_y = self.generate_orbital_data(
            st.session_state.time * speed_multiplier, 
            self.venus_radius, 
            self.venus_orbital_period
        )

        # Orbital paths
        if show_orbits:
            # Earth orbit
            earth_orbit_x = self.earth_radius * np.cos(np.linspace(0, 2*np.pi, 200))
            earth_orbit_y = self.earth_radius * np.sin(np.linspace(0, 2*np.pi, 200))
            fig.add_trace(go.Scatter(
                x=earth_orbit_x, y=earth_orbit_y, 
                mode='lines',
                line=dict(color='blue', dash='dot'),
                name='Earth Orbit'
            ))

            # Venus orbit
            venus_orbit_x = self.venus_radius * np.cos(np.linspace(0, 2*np.pi, 200))
            venus_orbit_y = self.venus_radius * np.sin(np.linspace(0, 2*np.pi, 200))
            fig.add_trace(go.Scatter(
                x=venus_orbit_x, y=venus_orbit_y, 
                mode='lines',
                line=dict(color='red', dash='dot'),
                name='Venus Orbit'
            ))

        # Planets
        fig.add_trace(go.Scatter(
            x=[earth_x], y=[earth_y], 
            mode='markers',
            marker=dict(color='blue', size=15),
            name='Earth'
        ))
        
        fig.add_trace(go.Scatter(
            x=[venus_x], y=[venus_y], 
            mode='markers',
            marker=dict(color='red', size=10),
            name='Venus'
        ))

        # Layout
        fig.update_layout(
            title='Venus Transit Orbital Simulation',
            xaxis_title='Astronomical Units (AU)',
            yaxis_title='Astronomical Units (AU)',
            height=600,
            width=800,
            showlegend=True
        )

        # Display the plot using placeholders
        plot_placeholder.plotly_chart(fig, use_container_width=True)

        # Check for transit
        is_transit = self.is_transit_occurring(earth_x, earth_y, venus_x, venus_y)
        
        # Display time and position information
        with info_placeholder.container():
            # Create columns for information display
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown(f"""
                ### Simulation Details
                - **Current Time**: {st.session_state.time} days
                - **Earth Position**: ({earth_x:.2f}, {earth_y:.2f})
                - **Venus Position**: ({venus_x:.2f}, {venus_y:.2f})
                """)
            
            with info_col2:
                if is_transit:
                    st.warning("🔴 TRANSIT IN PROGRESS")
                    st.markdown("#### Transit Characteristics")
                    st.markdown("""
                    - Planets aligned with Sun
                    - Venus appears as a small dark spot
                    - Visible for several hours
                    """)
                else:
                    st.success("No Active Transit")

        # Pause to control animation speed
        time.sleep(0.1)

        # Auto-play mechanism
        if st.session_state.is_playing:
            st.rerun()
            #st.experimental_rerun()

def main():
    simulation = VenusTransitSimulation()
    simulation.create_simulation()

if __name__ == '__main__':
    main()
