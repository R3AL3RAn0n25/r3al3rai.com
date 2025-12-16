"""Generated Physics Knowledge Base - Import into prompts.py"""

PHYSICS_KNOWLEDGE_BASE = {
    "physics_problem_1": """An idealized Atwood machine (massless pulley and string) connected to two blocks of masses M and 2M sits initially at rest on a flat horizontal table. The coefficient of static and kinetic friction, a... Answer: (a) The distances traveled by the blocks from their initial resting points as a function of time are:
- For the block of mass M:
  x₁(t) = (1/6)(4A + μg)t²
- For the block of mass 2M, assuming it move...""",
    "physics_problem_2": """A small block of mass $m$ lies above a thin disk of total mass $M$, constant surface density $\sigma$, and radius R. A hole of radius R/2 is cut into the center of the disk, creating an annulus. The m... Answer: (a) The net force on the block for a small vertical displacement `Δh` is `F_z = -(2πGσ/R) * m * Δh`. This is a linear restoring force of the form `F = -kx`, so the block undergoes simple harmonic moti...""",
    "physics_problem_3": """A uniform bar of mass M, length L, and negligible width and thickness is pivoted about a fixed post at a point 1/3 along the length of the bar. The bar is initially released from rest when it is tippe... Answer: (a) The total force the swinging bar exerts on the fixed post when it passes through horizontal is `F = Mg * ( (1/2)x̂ - (3/4)ẑ )`.
(b) The angular rotation rate of the bar as it swings past its lowe...""",
    "physics_problem_4": """A billiards player strikes a cue ball (a uniform sphere with mass $M$ and radius $R$ ) with a cue stick. The strike occurs at the horizontal midpoint of the ball (i.e., at a height R above the table) ... Answer: (a) The initial speed of the cue ball is $v_0 = \frac{\Delta p}{M} \cos\alpha$, and its initial angular rotation rate is $\omega_0 = \frac{5}{2} \frac{\Delta p}{MR} \sin\alpha$.

(b) For the ball to e...""",
    "physics_problem_5": """An Atwood machine consists of a massive pulley (a uniform circular disk of mass M and radius R) connecting two blocks of masses M and M/2. Assume that the string connecting the two blocks has negligib... Answer: (a) The net accelerations of the two blocks in an inertial frame of reference (with upward defined as the positive direction) are:
-   Acceleration of the block with mass M: `a₁ = (3A - g) / 4`
-   Ac...""",
    "physics_problem_6": """Two students, each of mass M, are attempting to push a block of mass 2M up a symmetric triangular hill with opening angle 2α. Student A pushes the load straight up, and student B pulls the load up usi... Answer: The relationship is `cot(α_min) = μ₂`....""",
    "physics_problem_7": """Two students, each of mass M, are attempting to push a block of mass 2M up a symmetric triangular hill with an opening angle of 2α. Student A pushes the load straight up the hill. Student B pulls the ... Answer: The force `F` that each student must exert to move the block at a constant velocity is the same for both:
F = 2Mg(μ₂sin(α) + cos(α))

However, Student B has a significant advantage. To exert this forc...""",
    "physics_problem_8": """Two students, each of mass M, are attempting to push a block of mass 2M up a symmetric triangular hill with opening angle 2α. Student A pushes the load straight up; student B pulls the load up by runn... Answer: The maximum angle of inclination for each student is given by:

-   Student A (pushing):  `cot(α_A) = 3 / (μ₁ - 2μ₂)`
-   Student B (pulling): `cot(α_B) = 1 / (μ₁ - 2μ₂)`

Since `cot(α_A) > cot(α_B)`,...""",
    "physics_problem_9": """A solid uniform ball (a sphere) of mass M and radius R rolls in a bowl that has a radius of curvature L, where L > R. Assume that the ball rolls without slipping, and that constant gravitational accel... Answer: (a) The equation of motion for the angle θ is:
`d²θ/dt² = - (5g / 7(L-R)) * sin(θ)`

(b) For small angles, the position of the ball as a function of time is:
`θ(t) = θ₀ * cos(ωt)`, where the angular f...""",
    "physics_problem_10": """A small asteroid of mass $m$ moves with speed $v$ when it is far away from a large planet of mass M. The "impact parameter", b, is the distance between the centers of mass of the planet and asteroid p... Answer: (a) The minimum impact parameter $b_{min}$ for the asteroid to just miss the planet is found by applying conservation of energy and angular momentum.
The result is:
$b_{min} = R \sqrt{1 + \frac{2GM}{R...""",
    "physics_problem_11": """A gyroscope wheel consists of a uniform disk of mass M and radius R that is spinning at a large angular rotation rate $\omega_s$. The gyroscope wheel is mounted onto a ball-and-socket pivot by a rod o... Answer: (a) The total angular momentum vector is:
$\vec{L} = \frac{1}{2} M R^2 \omega_s \hat{x} + M\left(\frac{1}{4} R^2 + D^2\right) \frac{2 D g}{R^2 \omega_s} \hat{z}$

(b) With upward acceleration A, the p...""",
    "physics_problem_12": """A bowling ball of radius R, mass M, and uniform mass density is thrown down a lane with initial horizontal speed $\mathrm{v}_0$. The ball is given some backspin - it is spun in the opposite direction ... Answer: (a) The velocity and angular rotation rate of the ball as a function of time (while slipping) are:
$\vec{v}(t) = (v_0 - \mu g t)\hat{x}$
$\omega(t) = \omega_0 - \frac{5}{2}\frac{\mu g}{R}t$ (where pos...""",
    "physics_problem_13": """Consider the following force law:

F(x) = (mc²/4) * ( (4a²/x³) - (3a³/x⁴) - (a/x²) )

for x > 0, where m is the mass of the object, a is a constant length and c is the speed of light.
(a) Sketch the p... Answer: (a) The potential energy is U(x) = (mc²/4) * ( (2a²/x²) - (a³/x³) - (a/x) ) + U₀. The two finite equilibrium points are found by setting F(x)=0, which yields x=a and x=3a. By analyzing the second deri...""",
    "physics_problem_14": """A small block starts from rest and slides down from the top of a fixed sphere of radius R, where R is much larger than the size of the block. The surface of the sphere is frictionless and a constant g... Answer: (a) The speed of the block as a function of the angle θ is given by the expression `v = sqrt(2gR(1 - cos(θ)))`.

(b) The block loses contact with the sphere when the normal force becomes zero. This oc...""",
    "physics_problem_15": """A rocket of total mass M₀, half of which is fuel, starts at rest on a long horizontal table. The coefficient of friction between the rocket and table surfaces is μ. At time t=0, the rocket is ignited,... Answer: (a) The condition for the rocket to start moving is that the thrust must overcome the initial static friction.
Thrust > Max Static Friction
**γ * v_ex > μM₀g**

(b) The maximum speed is achieved when ...""",
    "physics_problem_16": """A flyball governor is shown in the diagram below. A rotating shaft is connected to two hinges of mass $M$ through rigid, massless rods of length $L$. The rods are also attached at the bottom to a larg... Answer: (a) The height of the large block above its non-rotating position as a function of $\omega$ is:
$h = 2L\left(1 - \frac{4g}{L\omega^2}\right)$

(b) The expression relating the vertical speed of the blo...""",
    "physics_problem_17": """A cylindrical mass $M$ is placed on a post connected to a rotating shaft. The post forces the mass to rotate with the shaft at a constant angular velocity $\Omega$. The mass is connected to the shaft ... Answer: (a) The equilibrium distance of the mass from the central shaft is:
$r_{eq} = \frac{kL}{k - M\Omega^2}$

(b) The period of oscillation is given by $T = \frac{2\pi}{\omega}$, where the angular frequenc...""",
    "physics_problem_18": """Two blocks of masses $M_1$ and $M_2$ (where $M_2 > M_1$) are stacked on top of each other and start at rest on the surface of a frictionless table. The masses are connected via an ideal string and pul... Answer: 1.  **No-slip condition:** If the blocks do not slip, they move together. Their accelerations are equal to the acceleration of the pulley: $a_1 = a_2 = a$.

2.  **Slipping condition:** If the blocks s...""",
    "physics_problem_19": """Two sticks are attached with frictionless hinges to each other and to a wall, as shown in the image below. The angle between the sticks is $\theta$. Both sticks have the same constant linear mass dens... Answer: The force that the lower stick applies to the upper one at point A has two components:
-   **Vertical component:** $F_v = \frac{1}{2} \lambda L g$ (directed downwards)
-   **Horizontal component:** $F...""",
    "physics_problem_20": """An idealized Atwood machine, consisting of two blocks of masses M and 3M connected via a massless string through a massless pulley, sits on a flat horizontal table. The coefficient of kinetic friction... Answer: (a) The horizontal accelerations of the two masses in the frame of rest of the table are:
- Acceleration of mass M: `a_M = (3/2)A + (1/2)μg`
- Acceleration of mass 3M: `a_3M = (1/2)A - (1/2)μg`
(Assum...""",
    "physics_problem_21": """A platform of mass M and uniform density rests on three solid cylinders, each of mass M, radius R and uniform density. The whole structure is initially at rest on an inclined plane tilted at angle θ, ... Answer: (a) The acceleration of the platform with solid cylinders is **(20/17)g sin(θ)**.

(b) The acceleration of the platform with hollow cylinders is **g sin(θ)**.

(c) The optimal rollers are **(3) cylind...""",
    "physics_problem_22": """A block of mass $M$ sits on an inclined plane and is connected via a massless string through a massless pulley A (that slides without friction on the plane) to a fixed post. This pulley is in turn con... Answer: By applying Newton's second law to the massless pulley A, we find that the net force on it must be zero. Summing the forces parallel to the inclined plane gives the equation $T_2 - 2T_1 = 0$. Therefor...""",
    "physics_problem_23": """A block of mass $M$ sits on an inclined plane and is connected via a massless string through a massless, frictionless pulley A to a fixed post. Pulley A is, in turn, connected via another massless str... Answer: The relation for the minimum angle $\theta$ as a function of $\mu$ is:
$1 = \mu \cos\theta + \sin\theta$...""",
    "physics_problem_24": """A tunnel is built connecting two spots on the Earth that follows a straight trajectory through the interior but does not intersect the center of the Earth. A student falls into the tunnel. Assume that... Answer: The equation of motion for the student in the tunnel is `d^2x/dt^2 = - (GM/R^3) * x`. This is the standard form of the equation for Simple Harmonic Motion, `d^2x/dt^2 = -ω^2 * x`, with an angular freq...""",
    "physics_problem_25": """A tunnel is built connecting two spots on the Earth that follows a straight trajectory through the interior, but does not intersect the center of the Earth. A student falls into the tunnel. Assume tha... Answer: 1.  **Proof of Simple Harmonic Motion:**
    The gravitational force on a mass `m` at a distance `r` from the center of a uniform Earth is `F_g = -(GmM/R³)r`. The component of this force along the tun...""",
    "physics_problem_26": """A bowling ball of radius R, mass M, and uniform mass density is thrown down a lane with an initial horizontal speed of v₀. The ball is given backspin with an initial angular rate of ω₀, as shown in th... Answer: (a) The velocity and angular rotation rate of the ball as a function of time, while it is slipping, are:
-   Velocity: `v(t) = v₀ - μgt`
-   Angular Velocity: `ω(t) = ω₀ - (5μg / 2R)t`
(Here, v is pos...""",
    "physics_problem_27": """A coin, which is a uniform solid circular disk with mass $M$ and radius $b$, is set to roll in a circular path of radius $R$ on a horizontal table surface, where $R > b$. The coin is given a spin angu... Answer: The final expression for the tilt angle $\alpha$ is given by:
$$ \tan\alpha = \frac{3b^2\omega_s^2}{2gR} $$...""",
    "physics_problem_28": """A coin, which is a uniform solid circular disk with mass $M$ and radius $b$, is set to roll in a circular path of radius $R$ on a table surface, where $R > b$. The coin is given a spin angular velocit... Answer: (a) The precession angular velocity has magnitude $\Omega = \omega_s \frac{b}{R}$ and its direction is vertically upward ($\hat{z}$).

(b) The total angular velocity vector is $\vec{\omega} = \omega_s...""",
    "physics_problem_29": """An Atwood machine consists of a fixed pulley wheel of radius R and uniform mass M (a disk), around which an effectively massless string passes connecting two blocks of mass M and 2M. The lighter block... Answer: (a) The conditions for the lighter block to move are:
-   To move down: `sin(α) + μcos(α) < 1/2`
-   To move up: `sin(α) - μcos(α) > 1/2`

(b) Assuming the lighter block moves down, its acceleration `...""",
    "physics_problem_30": """A cylindrical rocket of diameter $2R$, mass $M_R$ and containing fuel of mass $M_F$ is coasting through empty space at velocity $v_0$. At some point the rocket enters a uniform cloud of interstellar p... Answer: (a) The equation of motion of the rocket is:
$$ \left(M_R+M_F-\gamma t\right) \frac{dv}{dt}=\gamma u-A v^2 $$

(b) To maintain a constant velocity $v_0$, the rocket's thrust must be equal to the drag ...""",
    "physics_problem_31": """A cylinder of mass M, length L, and radius R is spinning about its long axis with angular velocity $\vec{\omega}=\omega_s \hat{x}$ on a frictionless horizontal surface. The cylinder is given a sharp, ... Answer: (a) The translational velocity of the cylinder's center of mass after the impulse has a magnitude of $\frac{\Delta p}{M}$ and is in the positive $\hat{y}$ direction.
$\vec{v} = \frac{\Delta p}{M} \hat...""",
    "physics_problem_32": """A cylinder of mass M, length L, and radius R is spinning about its long axis with angular velocity $\vec{\omega}=\omega_s \hat{x}$ on a frictionless horizontal surface. The cylinder is given a sharp, ... Answer: The precessional rate is $\Omega = \frac{Lg}{R^2 \omega_s}$.
The direction of precession is vertically upward (along the $\hat{z}$-axis), which corresponds to a counter-clockwise rotation when viewed ...""",
    "physics_problem_33": """A cylinder of mass M, length L, and radius R is spinning about its long axis with angular velocity $\vec{\omega}=\omega_s \hat{x}$ on a frictionless horizontal surface. The cylinder is given a sharp, ... Answer: The condition for the cylinder to precess in the opposite direction is that its tilt angle, $\alpha$, must be greater than a critical angle, $\alpha_c$, defined by the cylinder's geometry.

The minimu...""",
    "physics_problem_34": """Consider the system depicted in the diagram below. A block with a mass of $m_1=7.4$ kg is situated on a frictionless ramp, which is inclined at an angle of $45°$. This block is connected by a rope tha... Answer: The calculated acceleration of the system is $a = -0.03$ m/s², where the negative sign signifies that mass $m_1$ slides down the incline. The corresponding tension in the connecting rope is $T = 51.09...""",
    "physics_problem_35": """Consider the setup depicted in the image, where a block with mass $m_1=6.2$ kg is positioned on a frictionless incline angled at $30^\circ$. This block is tethered by a rope that passes over a frictio... Answer: Based on the analysis of the forces and the application of Newton's second law, the acceleration of the system is calculated to be $a = 3.34$ m/s², and the tension in the rope connecting the two masse...""",
    "physics_problem_36": """Consider the arrangement illustrated in the provided diagram, featuring a block of mass $m_1=5.5$ kg on a frictionless plane inclined at $55^\circ$. This block is connected by an inextensible rope pas... Answer: Based on the analysis, the acceleration of the system is determined to be $a = 1.76$ m/s², and the tension in the rope connecting the two masses is $T = 53.85$ N....""",
    "physics_problem_37": """Consider the arrangement illustrated in the diagram below, where a block with mass $m_1 = 5.4$ kg is placed on a frictionless incline angled at $40^\circ$. This block is connected by a light, inextens... Answer: Based on the application of Newton's laws of motion, the calculated acceleration of the system is $a = 1.11$ m/s², and the tension in the rope connecting the two masses is $T = 39.99$ N....""",
    "physics_problem_38": """Consider the system depicted in the diagram below, where a block with mass $m_1=4.6$ kg sits on a frictionless plane inclined at an angle of $55°$. This block is tethered by a rope that passes over an... Answer: Based on the application of Newton's laws of motion, the acceleration of the system is determined to be $2.61 \text{ m/s}^2$, and the tension in the rope connecting the two masses is $48.92 \text{ N}$...""",
    "physics_problem_39": """Consider the system depicted in the image below, where a mass $m_1$ of $9.1$ kg is positioned on a frictionless incline angled at $55^\circ$. This mass is tethered by a rope that passes over an ideal ... Answer: The system accelerates at a rate of $a = 0.73$ m/s², with mass $m_1$ moving down the incline and mass $m_2$ moving upward. The tension in the connecting rope is $T = 66.37$ N. Note that if the positiv...""",
    "physics_problem_40": """Consider the system depicted in the diagram below, featuring a mass $m_1$ of 7.6 kg resting on a frictionless plane inclined at a 40° angle. This mass is linked by a rope passing over a frictionless p... Answer: The calculated acceleration of the system is $a = -0.84$ m/s², where the negative sign signifies that mass $m_1$ slides down the incline. The tension in the rope connecting the two masses is $T = 41.4...""",
    "physics_problem_41": """Consider the setup depicted below, where a block with mass $m_1 = 7.3$ kg is placed on a frictionless incline angled at $20^\circ$. This block is tethered by a rope that passes over a frictionless, ma... Answer: Based on the analysis of the forces and applying Newton's second law, the acceleration of the system is calculated to be $3.36 \text{ m/s}^2$, and the corresponding tension in the connecting rope is $...""",
    "physics_problem_42": """Consider the physical setup illustrated in the diagram below. A block with mass $m_1 = 1.1$ kg is placed on a frictionless incline angled at $40^\circ$. It is connected by a lightweight, inextensible ... Answer: The calculated acceleration of the system is $a = 7.34$ m/s², and the tension in the rope connecting the two masses is $T = 15.00$ N....""",
    "physics_problem_43": """Consider the system depicted in the image below, where a mass $m_1$ of 4.3 kg is positioned on a frictionless incline angled at 20°. This mass is tethered by a rope, which passes over a frictionless p... Answer: Based on the application of Newton's second law to the system, the acceleration of the masses is $a = 1.83$ m/s², and the tension in the connecting rope is $T = 22.30$ N....""",
    "physics_problem_44": """Consider the arrangement depicted in the image below. A block with mass $m_1=6.8$ kg is positioned on a frictionless ramp inclined at an angle of $20^\circ$. This block is tethered by a string that pa... Answer: The calculated acceleration for the system is $a = 1.81$ m/s², and the tension in the connecting rope is $T = 35.13$ N....""",
    "physics_problem_45": """For the system depicted in the diagram, where a mass $m_1$ of 6.1 kg is positioned on a frictionless incline angled at $55^\circ$ and connected by a rope over a pulley to a second hanging mass $m_2$ o... Answer: The acceleration of the system is calculated to be $0.89 \text{ m/s}^2$, and the tension in the rope connecting the two masses is $54.37 \text{ N}$....""",
    "physics_problem_46": """Consider the setup depicted in the image below, where a block with mass $m_1=6.1$ kg is positioned on a frictionless incline angled at $25°$. This block is tethered by a rope that passes over a fricti... Answer: The calculated acceleration of the system is $a = -1.24$ m/s², where the negative sign indicates that mass $m_1$ accelerates down the incline. The tension in the connecting rope is found to be $T = 17...""",
    "physics_problem_47": """As depicted in the diagram, a mass $m_1$ of 5.0 kg is positioned on a frictionless incline angled at 25 degrees. It is linked by a rope, which passes over a frictionless pulley, to a second, hanging m... Answer: Based on the application of Newton's Second Law, the acceleration of the system is determined to be $a = 0.86$ m/s², and the tension in the rope connecting the two masses is $T = 25.02$ N....""",
    "physics_problem_48": """Consider the system depicted in the image, featuring a mass $m_1=5.0$ kg positioned on a frictionless plane inclined at a $60^\circ$ angle. This mass is linked by a rope passing over a frictionless, m... Answer: The calculated acceleration of the system is $a = -0.59$ m/s², where the negative sign indicates that mass $m_1$ moves down the incline, contrary to the initially assumed positive direction. The tensi...""",
    "physics_problem_49": """A block with mass $m_1=8.9$ kg is positioned on a frictionless ramp inclined at an angle of $30°$. It is connected by a lightweight rope, which passes over a frictionless pulley, to a second block of ... Answer: The acceleration of the system is $a = -2.66$ m/s², where the negative sign indicates that mass $m_1$ accelerates down the incline. The tension in the rope connecting the two masses is $T = 19.94$ N....""",
    "physics_problem_50": """A system consists of a mass $m_1$ of 1.5 kg resting on a frictionless incline angled at 45 degrees, tethered by a rope over a frictionless pulley to a second, hanging mass $m_2$ of 5.6 kg, as depicted... Answer: Therefore, after analyzing the forces and applying Newton's laws, the calculated acceleration of the system is $a = 6.27$ m/s², and the tension in the connecting rope is $T = 19.79$ N....""",
}
