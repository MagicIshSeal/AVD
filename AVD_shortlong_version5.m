% Matlab AVD m file explanation [(un)collapse by pressing the '-' or '+' ]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Inholland University of Applied Sciences - Delft %%%%%%%%%%%%%%%%%%%%%
%%% AVD 2024-2025, Performance, Aeronautical Engineering %%%%%%%%%%%%%%%%%
%%% Determine short and long period motion %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Created by JR van der Ploeg %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Version 5.0, 07-05-2025 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% B747 and Stol Transport aerodynamic coefficients are based on DATCOM %
%%% McDonnell Aircraft Company. (1978). USAF (United States Air Force) %%%
%%% stability and control DATCOM(Accession Number: ADB072483). %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% The methods used are based on: Birdsall, D. Flight Stability and %%%%%
%%% Automatic Control—2nd edition, RC Nelson. The McGraw-Hill Companies.%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%               __|__               %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%      ----o--o--(_)--o--o----      %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Description:
% This MATLAB script is designed to determine the short and long period 
% motion of aircraft based on aerodynamic parameters and flight conditions. 
% The script allows the user to define parameters for different aircraft 
% types; includes a Boeing 747 and a STOL transport aircraft for reference, 
% providing flexibility for analysis.
%
% Key functionalities include:
% - Calculation of aerodynamic derivatives based on flight parameters and 
% conditions.
% - Construction of the system matrix to characterize the longitudinal 
% dynamics.
% - Impulse response analysis to assess the aircraft's behavior in response 
% to control inputs.
% - Detailed visualizations of results, showcasing the dynamics of the 
% selected aircraft.
%
% Your Workflow:
% Chapter 1 Initialization: Clears the workspace and sets example inputs 
% for various aircraft.
%!   Task: -
% Chapter 2 Aircraft Definitions: Structures are defined to hold parameters 
% and coefficients aircraft.
%!   Task: 2.3 Custom aircraft parameters can be set by the user; new
% aircraft structs can be appended
% Chapter 3 Aircraft Selection
%!   Task: 3.1-3.4 Select/append aircraft for analysis
% Chapter 4 Computational Analysis: aerodynamic derivatives, system matrix 
% for longitudinal motion, and impulse response
%!   Task: 4.7 Select response type (step / impulse) (uncomment {ctrl+t} / 
%! comment {ctrl+r} as needed)
% Chapter 5 Results Display: Displays key results, including aerodynamic 
% derivatives, system matrix, steps response metrics, and plots the 
% aircraft's time response and pole-zero map.
%!   Task: 5.6 Toggle on or off the constraint plot
% Chapter 6 Function definitions
%!   Task: -

% Your workflow starts below:
%% 1. Make sure the workspace is empty
clc;
close all;
clear all;

%% 2. Inputs (B747, STOL Transport, and Your aircraft)
% 2.1 B747
% B747/Aircraft Parameters and Constants Structure B747
B747_lon_para = struct(...
    'rho', 1.225,                     ...       % [kg/m^3] air density
    'theta_0', 0,                     ...       % [rad] Initial pitch angle
    'U0', 165 * 1.68781 * 0.3048,     ...       % [m/s]
    'S', 5500 * 0.092903,             ...       % [m^2] Wing area
    'b', 195.68 * 0.3048,             ...       % [m] Wingspan
    'c', 27.31 * 0.3048,              ...       % [m] Mean aerodynamic chord
    'm', 564000 * 0.453592,           ...       % [kg] Mass
    'Iyy', 32.3e6 * 14.5939 * 0.3048^2, ...     % [kg*m^2] Moment of inertia 
    'Ixx', 14.3e6 * 14.5939 * 0.3048^2, ... 
    'Izz', 45.3e6 * 14.5939 * 0.3048^2, ... 
    'Ixz', -2.23e6 * 14.5939 * 0.3048^2  ...
);

% B747/Aerodynamic Coefficients Structure
B747_lon_coef = struct('C_L', 1.11, 'C_D', 0.102, 'C_L_a', 5.7, 'C_D_a', 0.66, ...
    'C_m_a', -1.26, 'C_L_da', 6.7, 'C_m_da', -3.2, 'C_L_hq', 5.4, 'C_m_hq', -20.8, ...
    'C_L_M', -0.81, 'C_m_M', 0.27, 'C_L_de', 0.338, 'C_m_de', -1.34);

% 2.2 STOL transport
% STOL transport/Aircraft Parameters and Constants Structure
STOLT_M037_10000ft_lon_para = struct(...
    'rho', 515.4*17.56/10^4,          ...   % [kg/m^3] air density
    'theta_0', 0,                     ...   % [rad] Initial pitch angle
    'U0', 127,                        ...   % [m/s]
    'S', 945 * 0.092903,             ...    % [m^2] Wing area
    'b', 96 * 0.3048,                ...    % [m] Wingspan
    'c', 10.1 * 0.3048,              ...    % [m] Mean aerodynamic chord
    'm', 40000 * 0.453592,           ...    % [kg] Mass
    'Iyy', 2.73e5 * 14.5939 * 0.3048^2, ... % [kg*m^2] Moment of inertia 
    'Ixx', 2.15e5 * 14.5939 * 0.3048^2, ... 
    'Izz', 4.47e5 * 14.5939 * 0.3048^2, ... 
    'Ixz', 0 * 14.5939 * 0.3048^2  ...
);

% STOL transport/Aircraft Parameters and Constants Structure 
STOLT_M037_10000ft_lon_coef = struct('C_L', 0.3, 'C_D', 0.036, 'C_L_a', 5.24, 'C_D_a', 0.67, ...
    'C_m_a', -0.78, 'C_L_da', 1.33, 'C_m_da', -6.05, 'C_L_hq', 7.83, 'C_m_hq', -35.6, ...
    'C_L_M', 0, 'C_m_M', 0, 'C_L_de', 0.465, 'C_m_de', -2.12);

% 2.3 Your Aircraft Inputs
% YOUR AIRCRAFT/Aircraft Parameters and Constants Structure
input_lon_para = struct(...
    'rho', 1.1,          ...                % [kg/m^3] air density
    'theta_0', 0,                     ...   % [rad] Initial pitch angle
    'U0', 50,                        ...    % [m/s]
    'S', 6,             ...                % [m^2] Wing area
    'b', 7.75,                ...             % [m] Wingspan
    'c', 0.83,              ...              % [m] Mean aerodynamic chord
    'm', 170,           ...                 % [kg] Mass
    'Iyy', 372.99*1.6, ...                        % [kg*m^2] Moment of inertia 
    'Ixx', 0, ... 
    'Izz', 0, ... 
    'Ixz', 0  ...
);

% YOUR AIRCRAFT/Aircraft Parameters and Constants Structure 
input_lon_coef = struct('C_L', 0.3358, 'C_D', 0.05, 'C_L_a', 5.58, 'C_D_a', 0.170, ...
    'C_m_a', -0.51, 'C_L_da', -1.53, 'C_m_da', -6.05, 'C_L_hq', 7.83, 'C_m_hq', -35.6, ...
    'C_L_M', 0, 'C_m_M', 0, 'C_L_de', 0.465, 'C_m_de', -2.12);


%% 3. Select the aircraft of interest
% 3.1 Append Names of the selected aircraft
Names = {'B747','STOLT','Your Aircraft'}; % Store names for plot legends

% 3.2 Append Parameter structures to compare [para-1, para-2, ..., para-n]
AircraftParams = [B747_lon_para, ...
                STOLT_M037_10000ft_lon_para, ...
                input_lon_para]; 

% 3.3 Append Parameter coefficients to compare [coef-1, coef-2, ..., coef-n]
AircraftCoefs = [B747_lon_coef, ...
                STOLT_M037_10000ft_lon_coef, ...
                input_lon_coef];    

% 3.4 Set colours to identify aircraft in the graphs ['color-1','color-2',... 'color-n']
colors = ['b', 'g', 'r', 'c', 'm', 'y']; % Define a set of colors for plotting

%% 4. Execute calculations
% 4.0 initialise for comparison
figure('Color', 'w'); % Open figure with white background for display
hold on % Make sure all plots take place in the same figure
sysArray = cell(length(AircraftParams), 1);   % cellArray to collect each state-space system information
polesArray = cell(length(AircraftParams), 1);   % cellArray to collect each pole system information

% 4.1 till 5.4 are in the main loop; 5.5 is appended
for i = 1:length(AircraftParams)  

    % 4.1 Compute Aerodynamic Derivatives
    [q, M] = computeDynamicConditions(AircraftParams(i));
    [aeroDerivatives] = computeAeroDerivatives(q,M, AircraftParams(i), AircraftCoefs(i));
    % 4.2 Calculate the system matrix for longitudinal motion
    Alon = createSystemMatrix(aeroDerivatives, AircraftParams(i));
    % 4.3 (optional) Get and display eigenvalues
    eigs = eig(Alon);
    % 4.4 Impulse Response Analysis
    Blon = [0; aeroDerivatives.Zde; aeroDerivatives.Mdestar; 0]/180*pi();   % Control input: 1 deg elevator deflection
    LonSS = ss(Alon, Blon, eye(size(Alon)), zeros(size(Blon)));             % State-space representation
    sysArray{i} = LonSS;                                                    % Store system in the sysArray
    polesArray{i} = pole(LonSS);                                            % Store system poles in polesArray
    % 4.5 Selection time range of interest
    Time = linspace(0, 100, 10000);                                         % Time [s] (start, stop, steps)
    % 4.6 Use stepinfo to calculate step response characteristics
    info = stepinfo(sysArray{i});
    % 4.7 Select type of response of interest   (either impulse or step)
    [response, ~] = impulse(sysArray{i}, Time);  %(uncomment {ctrl+t} / comment {ctrl+r} as needed)
    % [response, ~] = step(sysArray{i}, Time);   %(uncomment {ctrl+t} / comment {ctrl+r} as needed)
    
    %% 5. Display Results
    % 5.1 Display the Aerodynamic Derivatives
    dispDerivatives(aeroDerivatives,Names{i});
    % 5.2 Display the Alon matrix
    displaySystemMatrix(Alon, Names{i});
    % 5.3 Display the step response info:
    displayStepResponseInfo(info,Names{i}) 
    % 5.4 Plotting the Aircraft Response and the Pole-zero map of Aircraft systems
    plotAircraftResponse(Time, response, AircraftParams(i), Names, colors(i))
    fprintf('\n')
end

% 5.5 Plotting Pole-Zero Map for All Systems in subplot(2, 3, 6);
plotpzmap(sysArray, Names, colors)

% 5.6 Constraints for aircraft design (set to true to activate constraints).
AcceptablePoleLocation  = 'true';                  % 'true' = display figure, 'false' = off  
if AcceptablePoleLocation                           % Toggle on or off contrainsts
    Good = 'true';                     
    Acceptable = 'true'; 
    Bad = 'true';
    PlotConstraint(Good, Acceptable, Bad, polesArray, Names, colors) % Plot desired areas
end

%% 6. FUNCTIONS 
function [q, M] = computeDynamicConditions(AircraftParams)
    U0 = AircraftParams.U0;                     % Get the speed in m/s
    rho = AircraftParams.rho;                   % Get the air density in kg/m^3
    q = 0.5 * rho * U0^2;                       % Dynamic pressure
    a = 340;                                    % Sonic velocity in m/s
    M = U0 / a;                                 % Mach number
end

function [aeroDerivatives] = computeAeroDerivatives(q, M, AircraftParams ,AircraftCoefs)
   
    theta_0 = AircraftParams.theta_0;           % Initial pitch angle [rad]
    U0 = AircraftParams.U0;                     % Speed [m/s]
    S = AircraftParams.S;                       % Wing area [m^2]
    b = AircraftParams.b;                       % Wingspan [m]
    c = AircraftParams.c;                       % Mean aerodynamic chord [m]
    m = AircraftParams.m;                       % Mass [kg]
    Iyy = AircraftParams.Iyy;                   % Moment of inertia [kg*m^2]
    Ixx = AircraftParams.Ixx;                   % Moment of inertia [kg*m^2]
    Izz = AircraftParams.Izz;                   % Moment of inertia [kg*m^2]
    Ixz = AircraftParams.Ixz;                   % Moment of inertia [kg*m^2]

    % Aerodynamic Coefficients
    C_D   = AircraftCoefs.C_D;                  % Drag coefficient - Represents the drag force on the aircraft relative to the dynamic pressure and wing area.
    C_D_a = AircraftCoefs.C_D_a;                % Change in drag coefficient with respect to angle of attack - Represents how drag varies as the angle of attack changes.
    C_L   = AircraftCoefs.C_L;                  % Lift coefficient - Represents the lift force on the aircraft relative to the dynamic pressure and wing area.
    C_L_a = AircraftCoefs.C_L_a;                % Change in lift coefficient due to the change in angle of attack - Indicates how lift varies with changes in the angle of attack.
    C_L_da = AircraftCoefs.C_L_da;              % Change in lift coefficient due to the change in chaning AoA - Measures the response to how quickly the angle of attack itself is changing, focusing on the dynamics of lift as the pitch attitude changes. It considers the "rate" of change of angle, making it a dynamic response.
    C_L_hq = AircraftCoefs.C_L_hq;              % Change in lift coefficient with respect to pitch rate - Represents the effect of the aircraft's pitch rate on lift.
    C_L_M = AircraftCoefs.C_L_M;                % Change in lift coefficient with respect to Mach number - Indicates how lift varies as the aircraft's speed approaches the speed of sound.
    C_L_de = AircraftCoefs.C_L_de;              % Change in lift coefficient with respect to elevator deflection - Measures how lift changes due to adjustments in the elevator.
    C_m_a = AircraftCoefs.C_m_a;                % Change in pitching moment with respect to angle of attack - Indicates how the pitching moment varies as the angle of attack changes.
    C_m_da = AircraftCoefs.C_m_da;              % Change in pitching moment with respect to the change in angle of attack - Measures the effect changing angle of attack on the pitching moment.
    C_m_hq = AircraftCoefs.C_m_hq;              % Change in pitching moment with respect to pitch rate - Represents how the pitching moment is affected by the pitch rate.
    C_m_M = AircraftCoefs.C_m_M;                % Change in pitching moment with respect to Mach number - Indicates how the pitching moment varies as the aircraft's speed approaches the speed of sound.
    C_m_de = AircraftCoefs.C_m_de;              % Change in pitching moment with respect to elevator deflection - Measures the effect of elevator adjustments on the pitching moment.

    % Calculate derivatives
    Xu = -q * S / m / U0 * (2 * C_D);
    Xw = q * S / m / U0 * (C_L - C_D_a);
    Zu = -q * S / m / U0 * (2 * C_L + M * C_L_M);
    Zw = -q * S / m / U0 * (C_D + C_L_a);
    Zdw = q * S * c / m / (2 * U0^2) * C_L_da;
    Zq = -q * S * c / (2 * m * U0) * C_L_hq;
    Mu = q * S * c / Iyy / U0 * M * C_m_M;
    Mw = q * S * c / Iyy / U0 * C_m_a;
    Mdw = q * S * c^2 / (2 * Iyy * U0^2) * C_m_da;
    Mq = q * S * c^2 / (2 * Iyy * U0) * C_m_hq;
    Zde = -q * S / m * C_L_de;
    Mde = q * S * c / Iyy * C_m_de;

    % Calculate the new derived quantities
    Mustar = Mu + Mdw * Zu;
    Mwstar = Mw + Mdw * Zw;
    Mqstar = Mq + Mdw * Zq;
    Mthetastar = -Mdw * 9.80665 * sin(theta_0);
    Mdestar = Mde + Mdw * Zde;

    % Store in a structure
    aeroDerivatives = struct('Xu', Xu, 'Xw', Xw, 'Zu', Zu, 'Zw', Zw, ...
        'Zdw', Zdw, 'Zq', Zq, 'Mu', Mu, 'Mw', Mw, 'Mdw', Mdw, ...
        'Mq', Mq, 'Zde', Zde, 'Mde', Mde, 'Mustar', Mustar, 'Mwstar', Mwstar,...
        'Mqstar', Mqstar, 'Mthetastar', Mthetastar, 'Mdestar', Mdestar );
end

function dispDerivatives(aeroDerivatives, name) % Display aeroDerivatives
    fprintf('\nThe following aeroDerivatives are for... %s \n', name);
    fprintf('Xu = %.4f\n', aeroDerivatives.Xu);
    fprintf('Xw = %.4f\n', aeroDerivatives.Xw);
    fprintf('Zu = %.4f\n', aeroDerivatives.Zu);
    fprintf('Zw = %.4f\n', aeroDerivatives.Zw);
    fprintf('Zdw = %.4f\n', aeroDerivatives.Zdw);
    fprintf('Zq = %.4f\n', aeroDerivatives.Zq);
    fprintf('Mu = %.4f\n', aeroDerivatives.Mu);
    fprintf('Mw = %.4f\n', aeroDerivatives.Mw);
    fprintf('Mdw = %.4f\n', aeroDerivatives.Mdw);
    fprintf('Mq = %.4f\n', aeroDerivatives.Mq);
    fprintf('Zde = %.4f\n', aeroDerivatives.Zde);
    fprintf('Mde = %.4f\n', aeroDerivatives.Mde);
    fprintf('\n')
end

function Alon = createSystemMatrix(aeroDerivatives, AircraftParams) % Output A matrix longitudinal stick fixed motion
    U0 = AircraftParams.U0;         % Get the speed in m/s
    theta_0 = AircraftParams.theta_0;         % Get the speed in m/s
    % Create the system matrix for longitudinal motion
    Alon = [aeroDerivatives.Xu, aeroDerivatives.Xw, 0, -9.80665 * cos(theta_0);
            aeroDerivatives.Zu, aeroDerivatives.Zw, U0 + aeroDerivatives.Zq, -9.80665 * sin(theta_0);
            aeroDerivatives.Mu, aeroDerivatives.Mw, aeroDerivatives.Mq, aeroDerivatives.Mthetastar;
            0, 0, 1, 0]; 
end

function displaySystemMatrix(Alon, name) % Displays the system matrix for longitudinal motion.
    %   displaySystemMatrix(Alon) takes the system matrix Alon as input
    %   and displays it with a descriptive message.
    
    % Display message and the system matrix
    fprintf('The system matrix for longitudinal motion of %s is: \n', name);
    disp(Alon);
end

function displayStepResponseInfo(info, name) 
    % DISPLAYSTEPPRESPONSEINFO Displays the step response metrics.
    %   Displays rise_time, transient_time, settling_time, 
    %   settling_min, settling_max, overshoot, undershoot, peak, peak_time
    fprintf('\nThe following information is for... %s \n', name);
    dispname = {'Forward speed u [m/s]', 'Heave velocity w [m/s]', 'Pitch rate q [deg/s]', 'Pitch angle theta [deg]'}; 
    for i = 1:length(info)
        % Display the information for corresponding plot
        fprintf('Step Response information for... %s \n', dispname{i});
        % Display the results using the correct field names
        fprintf('Rise Time: %.4f seconds\n', info(i).RiseTime);
        fprintf('Transient Time: %.4f seconds\n', info(i).TransientTime);
        fprintf('Settling Time: %.4f seconds\n', info(i).SettlingTime);
        fprintf('Settling Minimum: %.4f\n', info(i).SettlingMin);
        fprintf('Settling Maximum: %.4f\n', info(i).SettlingMax);
        fprintf('Overshoot: %.4f%%\n', info(i).Overshoot);
        fprintf('Undershoot: %.4f%%\n', info(i).Undershoot);
        fprintf('Peak: %.4f\n', info(i).Peak);
        fprintf('Peak Time: %.4f seconds\n', info(i).PeakTime);
        fprintf('\n')
    end
end

function plotAircraftResponse(Time, response, AircraftParams, Names, color)
    U0 = AircraftParams.U0;         % Get the speed in m/s
    % Extract response variables
    u = response(:, 1);   % Forward Speed
    w = response(:, 2);   % Heave Velocity
    q = response(:, 3);   % Pitch Rate
    theta = response(:, 4); % Pitch Attitude
    alpha = rad2deg(w ./ (U0 + u)); % AoA alpha in degrees

    % Convert q and theta from radians to degrees
    q = rad2deg(q);
    theta = rad2deg(theta);

    % Plotting the results
    subplot(2, 3, 1);
    hold on; % Keep the current plot
    plot(Time, u, 'Color', color);
    title('Forward Speed');
    xlabel('Time (s)');
    ylabel('u (m/s)');
    legend(Names, 'Location', 'best'); % Set legend
    grid on;
    grid minor;

    subplot(2, 3, 2);
    hold on;
    plot(Time, w, 'Color', color);
    title('Heave Velocity');
    xlabel('Time (s)');
    ylabel('w (m/s)');
    legend(Names, 'Location', 'best'); % Set legend
    grid on;
    grid minor;
    
    subplot(2, 3, 3);
    hold on; 
    plot(Time, alpha, 'Color', color);
    title('Angle of Attack Over Time');
    xlabel('Time (s)');
    ylabel('\alpha (deg)');
    legend(Names, 'Location', 'best'); % Set legend
    grid on;
    grid minor;
    
    subplot(2, 3, 4);
    hold on; 
    plot(Time, q, 'Color', color);
    title('Pitch Rate');
    xlabel('Time (s)');
    ylabel('q (deg/s)');
    legend(Names, 'Location', 'best'); % Set legend
    grid on;
    grid minor;
    
    subplot(2, 3, 5);
    hold on; 
    plot(Time, theta, 'Color', color);
    title('Pitch Attitude');
    xlabel('Time (s)');
    ylabel('\theta (deg)');
    legend(Names, 'Location', 'best'); % Set legend
    grid on;
    grid minor;
end

function plotpzmap(sysArray, Names, colors)
    
    %%%%%%%%%% Constraints %%%%%%%%%%%%%% 
        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    subplot(2, 3, 6);
    hold on; % Keep the current plot

    % Color the background for stable (light orange) and unstable (light blue) regions
    fill([-10, 10, 10, -10], [-10, -10, 10, 10], [1, 0.8, 0.6], 'EdgeColor', 'none', 'FaceAlpha', 0.15); % Fill light orange
    fill([0, 10, 10, 0], [-10, -10, 10, 10], [0.68, 0.85, 0.9], 'EdgeColor', 'none', 'FaceAlpha', 0.3); % Fill light blue

    % Initialize arrays to hold all poles for x and y limits
    allRealParts = [];
    allImagParts = [];

    % Initialize a handle array for the legend
    poleHandles = gobjects(length(sysArray), 1); % Preallocate handles for poles

    % Loop through sysArray
    for i = 1:length(sysArray)
        poles = pole(sysArray{i});                  % poles
        allRealParts = [allRealParts; real(poles)]; % Append real parts
        allImagParts = [allImagParts; imag(poles)]; % Append imaginary parts

        % Plot pole location with assigned color and store the handle
        poleHandles(i) = plot(real(poles), imag(poles), 'x', ...
            'Color', colors(i), 'MarkerSize', 10, 'LineWidth', 2);
    end        

    % Determine the overall min and max for x and y axes
    real_min = min(allRealParts);
    real_max = max(allRealParts);
    imag_min = min(allImagParts);
    imag_max = max(allImagParts);
    
    % Set an offset for clarity
    offset = 0.1;

    % Setting the axis limits for the pole-zero plot
    xlim([real_min - offset, real_max + offset]); % Set x-axis limits
    ylim([imag_min - offset, imag_max + offset]); % Set y-axis limit

    % Set grid with lines of constant damping and natural frequency
    sgrid;

    % Plot legend for the poles using only the handles associated with them
    legend(poleHandles, Names, 'Location', 'best'); % Set legend using custom handles

    grid on; % Ensure the grid is on
    set(gca, 'GridColor', 'k'); % Set grid lines color to black
    set(gca, 'MinorGridColor', 'k'); % Set minor grid lines color to black

    xlabel('Real Part');
    ylabel('Imaginary Part');

end


function plotEllipse(centerX, centerY, a, b, theta, color, Area)
    t = linspace(0, 2*pi, 100);
    x_ellipse = a*cos(t);
    y_ellipse = b*sin(t);
    R = [cos(theta) -sin(theta); sin(theta) cos(theta)];
    coords = R * [x_ellipse; y_ellipse];
    x_plot = coords(1,:) + centerX;
    y_plot = coords(2,:) + centerY;
    plot(x_plot, y_plot, color, 'LineWidth', 2);
    text(centerX+ 0.5*a, centerY +0.6*b, Area, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
end

function PlotConstraint(Good, Acceptable, Bad, polesArray, Names, colors)
    figure; hold on;
    
    x_center_good = 0.72; y_center_good = 0.5; a_good=0.28; b_good=0.09; theta_good=deg2rad(5);
    x_center_accept = 0.75; y_center_accept=0.55; a_accept=0.37; b_accept=0.21; theta_accept=deg2rad(8);
    x_center_bad=0.85; y_center_bad=0.68; a_bad=0.6; b_bad=0.38; theta_bad=deg2rad(7);

    for i = 1:length(polesArray)
        poles = polesArray{i};

        % Store pairs (zeta, wn) with their indices
        pairs = [];
        
        j = 1;
        while j <= length(poles)
            s = poles(j);
            if ~isreal(s)
                s_conj = conj(s);
                idx_conj = find(abs(poles - s_conj) < 1e-8, 1);
                if ~isempty(idx_conj) && idx_conj > j
                    % Compute from average of the pair
                    s_avg = (s + s_conj)/2;
                    wn = abs(s_avg);
                    zeta = -real(s)/abs(s);
                    pairs(end+1, :) = [zeta, wn]; % Store pair info
                    j = idx_conj; % Skip the conjugate
                end
            end
            j = j + 1;
        end
        
        % Find the max ωₙ for this system
        if ~isempty(pairs)
            [~, idx_max] = max(pairs(:,2));
            zeta_max = pairs(idx_max,1);
            wn_max = pairs(idx_max,2);
            % Plot only the max ωₙ pair
            plot(zeta_max, wn_max, 'x', 'MarkerSize', 10, 'LineWidth', 3, 'Color', colors(i));

            % check which area
            % Initialize default state
            state = 'Unacceptable';
            
            insideGood = false;
            if Good
                insideGood = isInEllipse(zeta_max, wn_max, x_center_good, y_center_good, a_good, b_good, theta_good);
            end
            
            insideAcceptable= false;
            if Acceptable
                insideAcceptable= isInEllipse(zeta_max, wn_max, x_center_accept, y_center_accept, a_accept, b_accept, theta_accept);
            end
            
            insideBad= false;
            if Bad
                insideBad= isInEllipse(zeta_max, wn_max, x_center_bad, y_center_bad, a_bad, b_bad, theta_bad);
            end
            
            if insideGood
                state='good';
            elseif insideAcceptable
                state='acceptable';
            elseif insideBad
                state='bad';
            end
            
            fprintf('Short-Period of %s: Max ωn=%.3f, ζ=%.3f, Area: %s\n', Names{i}, wn_max, zeta_max, state);
            
        end
    end

   % Plot regions
    if Good
        plotEllipse(x_center_good, y_center_good, a_good, b_good, theta_good, 'g', 'Good');
    end

    if Acceptable
        plotEllipse(x_center_accept, y_center_accept, a_accept, b_accept, theta_accept, 'y', 'Acceptable');
    end

    if Bad
        plotEllipse(x_center_bad, y_center_bad, a_bad, b_bad, theta_bad, 'r' , 'Bad');
    end

    grid on;
    grid minor;
    legend( Names, 'Location', 'best'); % Set legend using custom handles
    xlabel('Damping ratio \zeta');
    ylabel('Natural frequency \omega_n (rad/sec)');
    hold off;
end

function inside = isInEllipse(x, y, x_center, y_center, a, b, theta)
    % Translate point to ellipse center
    dx = x - x_center;
    dy = y - y_center;
    % Rotate point by -theta
    cs = cos(-theta);
    ss = sin(-theta);
    x_rot = cs*dx - ss*dy;
    y_rot = ss*dx + cs*dy;
    % Check ellipse equation
    inside = (x_rot/a)^2 + (y_rot/b)^2 <= 1;
end

