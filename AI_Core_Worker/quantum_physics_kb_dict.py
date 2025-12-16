"""Quantum Physics Knowledge Base for R3ALER AI"""

QUANTUM_PHYSICS_KB = {
    "quantum_state_normalization_001_original": {
        "content": """Problem:
**Problem 1: Pure Quantum State Normalization**

Consider a qubit in the pure state |ψ⟩ = α|0⟩ + β|1⟩.

**Part (a)**: What constraint must the amplitudes α and β satisfy for this to be a valid quantum state?

**Part (b)**: Prove that for any complex numbers α and β satisfying this constraint, we have |α|² ≤ 1.

**Part (c)**: Explain the physical interpretation of |α|² and |β|².

Solution Approach:
1. Use the normalization condition |α|² + |β|² = 1
2. Apply Complex.normSq_nonneg to show |β|² ≥ 0  
3. Use linear arithmetic to conclude |α|² ≤ 1

Key Concepts: quantum states, normalization, probability amplitudes, complex numbers""",
        "category": "quantum_physics",
        "topic": "Quantum Physics - Pure Quantum State Normalization",
        "source": "HuggingFace englund/quantum-physics-vvuq-complete",
        "level": "graduate",
        "subcategory": "quantum_states",
    },
    "pauli_matrix_algebra_002_original": {
        "content": """Problem:
**Problem 2: Pauli Matrix Algebra**

The Pauli X matrix is σₓ = |0⟩⟨1| + |1⟩⟨0| = [[0,1],[1,0]].

**Part (a)**: Prove that σₓ² = I (Pauli X is involutory).

**Part (b)**: Show that σₓ is Hermitian: σₓ† = σₓ.

**Part (c)**: Explain why Hermiticity is required for quantum observables.

Solution Approach:
1. Define the Pauli X matrix explicitly
2. Compute the matrix product using ext and fin_cases
3. Verify each matrix element equals the identity

Key Concepts: Pauli matrices, involutory operators, Hermitian operators, quantum observables""",
        "category": "quantum_physics",
        "topic": "Quantum Physics - Pauli Matrix Algebraic Properties",
        "source": "HuggingFace englund/quantum-physics-vvuq-complete",
        "level": "graduate",
        "subcategory": "quantum_operators",
    },
    "measurement_probability_003_original": {
        "content": """Problem:
**Problem 3: Born Rule and Measurement Probabilities**

For a quantum state ρ and measurement operator M, the Born rule gives the probability P = Tr(ρM).

**Part (a)**: Prove that measurement probabilities are always non-negative: P ≥ 0.

**Part (b)**: For a complete set of measurement operators {M₁, M₂, ..., Mₙ} with Σᵢ Mᵢ = I, show that total probability equals 1: Σᵢ Tr(ρMᵢ) = 1.

**Part (c)**: Explain the physical significance of this probability conservation.

Solution Approach:
1. Use trace linearity: Tr(A + B) = Tr(A) + Tr(B)
2. Apply the completeness relation Σᵢ Mᵢ = I
3. Use the fact that Tr(ρI) = Tr(ρ)

Key Concepts: Born rule, measurement probability, POVM, probability conservation, trace""",
        "category": "quantum_physics",
        "topic": "Quantum Physics - Quantum Measurement Probabilities",
        "source": "HuggingFace englund/quantum-physics-vvuq-complete",
        "level": "graduate",
        "subcategory": "quantum_measurements",
    },
}
